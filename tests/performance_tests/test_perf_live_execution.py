# -------------------------------------------------------------------------------------------------
#  Copyright (C) 2015-2021 Nautech Systems Pty Ltd. All rights reserved.
#  https://nautechsystems.io
#
#  Licensed under the GNU Lesser General Public License Version 3.0 (the "License");
#  You may not use this file except in compliance with the License.
#  You may obtain a copy of the License at https://www.gnu.org/licenses/lgpl-3.0.en.html
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# -------------------------------------------------------------------------------------------------

import asyncio
import cProfile
import pstats
import time
import unittest

from nautilus_trader.analysis.performance import PerformanceAnalyzer
from nautilus_trader.common.clock import LiveClock
from nautilus_trader.common.logging import TestLogger
from nautilus_trader.common.uuid import UUIDFactory
from nautilus_trader.data.cache import DataCache
from nautilus_trader.execution.database import BypassExecutionDatabase
from nautilus_trader.live.execution_engine import LiveExecutionEngine
from nautilus_trader.model.commands import SubmitOrder
from nautilus_trader.model.enums import OrderSide
from nautilus_trader.model.identifiers import AccountId
from nautilus_trader.model.identifiers import PositionId
from nautilus_trader.model.identifiers import TraderId
from nautilus_trader.model.identifiers import Venue
from nautilus_trader.model.objects import Quantity
from nautilus_trader.trading.portfolio import Portfolio
from nautilus_trader.trading.strategy import TradingStrategy
from tests.test_kit.mocks import MockExecutionClient
from tests.test_kit.performance import PerformanceHarness
from tests.test_kit.providers import TestInstrumentProvider
from tests.test_kit.stubs import TestStubs


BTCUSDT_BINANCE = TestInstrumentProvider.btcusdt_binance()


class LiveExecutionPerformanceTests(unittest.TestCase):

    def setUp(self):
        # Fixture Setup
        self.clock = LiveClock()
        self.uuid_factory = UUIDFactory()
        self.logger = TestLogger(self.clock, bypass_logging=True)

        self.trader_id = TraderId("TESTER", "000")
        self.account_id = AccountId("BINANCE", "001")

        self.portfolio = Portfolio(
            clock=self.clock,
            logger=self.logger,
        )
        self.portfolio.register_cache(DataCache(self.logger))

        self.analyzer = PerformanceAnalyzer()

        # Fresh isolated loop testing pattern
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        database = BypassExecutionDatabase(trader_id=self.trader_id, logger=self.logger)
        self.exec_engine = LiveExecutionEngine(
            loop=self.loop,
            database=database,
            portfolio=self.portfolio,
            clock=self.clock,
            logger=self.logger,
        )

        exec_client = MockExecutionClient(
            venue=Venue("BINANCE"),
            account_id=self.account_id,
            exec_engine=self.exec_engine,
            clock=self.clock,
            logger=self.logger,
        )

        self.exec_engine.register_client(exec_client)
        self.exec_engine.process(TestStubs.event_account_state(self.account_id))

        self.strategy = TradingStrategy(order_id_tag="001")
        self.strategy.register_trader(
            TraderId("TESTER", "000"),
            self.clock,
            self.logger,
        )

        self.exec_engine.register_strategy(self.strategy)

    def submit_order(self):
        order = self.strategy.order_factory.market(
            BTCUSDT_BINANCE.symbol,
            OrderSide.BUY,
            Quantity("1.00000000"),
        )

        self.strategy.submit_order(order)

    def test_execute_command(self):
        order = self.strategy.order_factory.market(
            BTCUSDT_BINANCE.symbol,
            OrderSide.BUY,
            Quantity("1.00000000"),
        )

        command = SubmitOrder(
            order.symbol.venue,
            self.trader_id,
            self.account_id,
            self.strategy.id,
            PositionId.null(),
            order,
            self.uuid_factory.generate(),
            self.clock.utc_now(),
        )

        def execute_command():
            self.exec_engine.execute(command)

        PerformanceHarness.profile_function(execute_command, 10000, 1)
        # ~0.0ms / ~0.3μs / 253ns minimum of 10,000 runs @ 1 iteration each run.

    def test_submit_order(self):
        self.exec_engine.start()
        time.sleep(0.1)

        async def run_test():
            def submit_order():
                order = self.strategy.order_factory.market(
                    BTCUSDT_BINANCE.symbol,
                    OrderSide.BUY,
                    Quantity("1.00000000"),
                )

                self.strategy.submit_order(order)

            PerformanceHarness.profile_function(submit_order, 10000, 1)
        self.loop.run_until_complete(run_test())
        # ~0.0ms / ~32.3μs / 32260ns minimum of 10,000 runs @ 1 iteration each run.

    def test_submit_order_end_to_end(self):
        self.exec_engine.start()
        time.sleep(0.1)

        async def run_test():
            for _ in range(10000):
                order = self.strategy.order_factory.market(
                    BTCUSDT_BINANCE.symbol,
                    OrderSide.BUY,
                    Quantity("1.00000000"),
                )

                self.strategy.submit_order(order)

        stats_file = "perf_live_execution.prof"
        cProfile.runctx("self.loop.run_until_complete(run_test())", globals(), locals(), stats_file)
        s = pstats.Stats(stats_file)
        s.strip_dirs().sort_stats("time").print_stats()
