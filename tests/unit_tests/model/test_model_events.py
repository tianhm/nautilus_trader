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

import unittest

from nautilus_trader.core.uuid import uuid4
from nautilus_trader.model.currencies import USD
from nautilus_trader.model.currencies import USDT
from nautilus_trader.model.enums import LiquiditySide
from nautilus_trader.model.enums import OrderSide
from nautilus_trader.model.enums import OrderType
from nautilus_trader.model.enums import TimeInForce
from nautilus_trader.model.events import AccountState
from nautilus_trader.model.events import OrderAccepted
from nautilus_trader.model.events import OrderAmended
from nautilus_trader.model.events import OrderCancelReject
from nautilus_trader.model.events import OrderCancelled
from nautilus_trader.model.events import OrderDenied
from nautilus_trader.model.events import OrderExpired
from nautilus_trader.model.events import OrderFilled
from nautilus_trader.model.events import OrderInitialized
from nautilus_trader.model.events import OrderInvalid
from nautilus_trader.model.events import OrderRejected
from nautilus_trader.model.events import OrderSubmitted
from nautilus_trader.model.identifiers import AccountId
from nautilus_trader.model.identifiers import ClientOrderId
from nautilus_trader.model.identifiers import Exchange
from nautilus_trader.model.identifiers import ExecutionId
from nautilus_trader.model.identifiers import OrderId
from nautilus_trader.model.identifiers import PositionId
from nautilus_trader.model.identifiers import StrategyId
from nautilus_trader.model.identifiers import Symbol
from nautilus_trader.model.objects import Money
from nautilus_trader.model.objects import Price
from nautilus_trader.model.objects import Quantity
from tests.test_kit.providers import TestInstrumentProvider
from tests.test_kit.stubs import TestStubs
from tests.test_kit.stubs import UNIX_EPOCH


AUDUSD_SIM = TestInstrumentProvider.default_fx_ccy(TestStubs.symbol_audusd())


class EventTests(unittest.TestCase):

    def test_account_state_str_repr(self):
        # Arrange
        uuid = uuid4()
        event = AccountState(
            account_id=AccountId("SIM", "000"),
            balances=[Money(1525000, USD)],
            balances_free=[Money(1525000, USD)],
            balances_locked=[Money(0, USD)],
            info={},
            event_id=uuid,
            event_timestamp=UNIX_EPOCH,
        )

        # Act
        # Assert
        self.assertEqual(f"AccountState(account_id=SIM-000, "
                         f"free=[1,525,000.00 USD], locked=[0.00 USD], id={uuid})", str(event))
        self.assertEqual(f"AccountState(account_id=SIM-000, "
                         f"free=[1,525,000.00 USD], locked=[0.00 USD], id={uuid})", repr(event))

    def test_order_initialized(self):
        # Arrange
        uuid = uuid4()
        event = OrderInitialized(
            cl_ord_id=ClientOrderId("O-2020872378423"),
            strategy_id=StrategyId("SCALPER", "001"),
            symbol=Symbol("BTC/USDT", Exchange("BINANCE")),
            order_side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
            quantity=Quantity("0.561000"),
            time_in_force=TimeInForce.DAY,
            event_id=uuid,
            event_timestamp=UNIX_EPOCH,
            options={"Price": "15200.10"}
        )

        # Act
        # Assert
        self.assertEqual(f"OrderInitialized(cl_ord_id=O-2020872378423, id={uuid})", str(event))
        self.assertEqual(f"OrderInitialized(cl_ord_id=O-2020872378423, id={uuid})", repr(event))

    def test_order_invalid(self):
        # Arrange
        uuid = uuid4()
        event = OrderInvalid(
            cl_ord_id=ClientOrderId("O-2020872378423"),
            reason="DUPLICATE_CL_ORD_ID",
            event_id=uuid,
            event_timestamp=UNIX_EPOCH,
        )

        # Act
        # Assert
        self.assertEqual(f"OrderInvalid(cl_ord_id=O-2020872378423, "
                         f"reason='DUPLICATE_CL_ORD_ID', id={uuid})", str(event))
        self.assertEqual(f"OrderInvalid(cl_ord_id=O-2020872378423, "
                         f"reason='DUPLICATE_CL_ORD_ID', id={uuid})", repr(event))

    def test_order_denied(self):
        # Arrange
        uuid = uuid4()
        event = OrderDenied(
            cl_ord_id=ClientOrderId("O-2020872378423"),
            reason="SINGLE_ORDER_RISK_EXCEEDED",
            event_id=uuid,
            event_timestamp=UNIX_EPOCH,
        )

        # Act
        self.assertEqual(f"OrderDenied(cl_ord_id=O-2020872378423, "
                         f"reason='SINGLE_ORDER_RISK_EXCEEDED', id={uuid})", str(event))
        self.assertEqual(f"OrderDenied(cl_ord_id=O-2020872378423, "
                         f"reason='SINGLE_ORDER_RISK_EXCEEDED', id={uuid})", repr(event))

    def test_order_submitted(self):
        # Arrange
        uuid = uuid4()
        event = OrderSubmitted(
            account_id=AccountId("SIM", "000"),
            cl_ord_id=ClientOrderId("O-2020872378423"),
            submitted_time=UNIX_EPOCH,
            event_id=uuid,
            event_timestamp=UNIX_EPOCH,
        )

        # Act
        self.assertEqual(f"OrderSubmitted(account_id=SIM-000, "
                         f"cl_ord_id=O-2020872378423, id={uuid})", str(event))
        self.assertEqual(f"OrderSubmitted(account_id=SIM-000, "
                         f"cl_ord_id=O-2020872378423, id={uuid})", repr(event))

    def test_order_rejected(self):
        # Arrange
        uuid = uuid4()
        event = OrderRejected(
            account_id=AccountId("SIM", "000"),
            cl_ord_id=ClientOrderId("O-2020872378423"),
            rejected_time=UNIX_EPOCH,
            reason="INSUFFICIENT_MARGIN",
            event_id=uuid,
            event_timestamp=UNIX_EPOCH,
        )

        # Act
        self.assertEqual(f"OrderRejected(account_id=SIM-000, cl_ord_id=O-2020872378423, "
                         f"reason='INSUFFICIENT_MARGIN', id={uuid})", str(event))  # noqa
        self.assertEqual(f"OrderRejected(account_id=SIM-000, cl_ord_id=O-2020872378423, "
                         f"reason='INSUFFICIENT_MARGIN', id={uuid})", repr(event))  # noqa

    def test_order_accepted(self, order_id=None):
        if order_id is None:
            order_id = OrderId("123456")

        # Arrange
        uuid = uuid4()
        event = OrderAccepted(
            account_id=AccountId("SIM", "000"),
            cl_ord_id=ClientOrderId("O-2020872378423"),
            order_id=order_id,
            accepted_time=UNIX_EPOCH,
            event_id=uuid,
            event_timestamp=UNIX_EPOCH,
        )

        # Act
        self.assertEqual(f"OrderAccepted(account_id=SIM-000, cl_ord_id=O-2020872378423, "
                         f"order_id={123456}, id={uuid})", str(event))  # noqa
        self.assertEqual(f"OrderAccepted(account_id=SIM-000, cl_ord_id=O-2020872378423, "
                         f"order_id={123456}, id={uuid})", repr(event))  # noqa

    def test_order_cancel_reject(self):
        # Arrange
        uuid = uuid4()
        event = OrderCancelReject(
            account_id=AccountId("SIM", "000"),
            cl_ord_id=ClientOrderId("O-2020872378423"),
            order_id=OrderId("123456"),
            rejected_time=UNIX_EPOCH,
            response_to="O-2020872378423",
            reason="ORDER_DOES_NOT_EXIST",
            event_id=uuid,
            event_timestamp=UNIX_EPOCH,
        )

        # Act
        self.assertEqual(f"OrderCancelReject(account_id=SIM-000, cl_ord_id=O-2020872378423, "
                         f"response_to=O-2020872378423, reason='ORDER_DOES_NOT_EXIST', "
                         f"id={uuid})", str(event))
        self.assertEqual(f"OrderCancelReject(account_id=SIM-000, cl_ord_id=O-2020872378423, "
                         f"response_to=O-2020872378423, reason='ORDER_DOES_NOT_EXIST', "
                         f"id={uuid})", repr(event))

    def test_order_cancelled(self):
        # Arrange
        uuid = uuid4()
        event = OrderCancelled(
            account_id=AccountId("SIM", "000"),
            cl_ord_id=ClientOrderId("O-2020872378423"),
            order_id=OrderId("123456"),
            cancelled_time=UNIX_EPOCH,
            event_id=uuid,
            event_timestamp=UNIX_EPOCH,
        )

        # Act
        self.assertEqual(f"OrderCancelled(account_id=SIM-000, cl_ord_id=O-2020872378423, "
                         f"order_id=123456, id={uuid})", str(event))
        self.assertEqual(f"OrderCancelled(account_id=SIM-000, cl_ord_id=O-2020872378423, "
                         f"order_id=123456, id={uuid})", repr(event))

    def test_order_amended(self):
        # Arrange
        uuid = uuid4()
        event = OrderAmended(
            account_id=AccountId("SIM", "000"),
            cl_ord_id=ClientOrderId("O-2020872378423"),
            order_id=OrderId("123456"),
            quantity=Quantity(500000),
            price=Price('1.95000'),
            amended_time=UNIX_EPOCH,
            event_id=uuid,
            event_timestamp=UNIX_EPOCH,
        )

        # Act
        self.assertEqual(f"OrderAmended(account_id=SIM-000, cl_order_id=O-2020872378423, "
                         f"order_id=123456, qty=500,000, price=1.95000, id={uuid})", str(event))
        self.assertEqual(f"OrderAmended(account_id=SIM-000, cl_order_id=O-2020872378423, "
                         f"order_id=123456, qty=500,000, price=1.95000, id={uuid})", repr(event))

    def test_order_expired(self):
        # Arrange
        uuid = uuid4()
        event = OrderExpired(
            account_id=AccountId("SIM", "000"),
            cl_ord_id=ClientOrderId("O-2020872378423"),
            order_id=OrderId("123456"),
            expired_time=UNIX_EPOCH,
            event_id=uuid,
            event_timestamp=UNIX_EPOCH,
        )

        # Act
        self.assertEqual(f"OrderExpired(account_id=SIM-000, cl_ord_id=O-2020872378423, "
                         f"order_id=123456, id={uuid})", str(event))
        self.assertEqual(f"OrderExpired(account_id=SIM-000, cl_ord_id=O-2020872378423, "
                         f"order_id=123456, id={uuid})", repr(event))

    def test_order_filled(self):
        # Arrange
        uuid = uuid4()
        event = OrderFilled(
            account_id=AccountId("SIM", "000"),
            cl_ord_id=ClientOrderId("O-2020872378423"),
            order_id=OrderId("123456"),
            execution_id=ExecutionId("1"),
            position_id=PositionId("2"),
            strategy_id=StrategyId("SCALPER", "001"),
            symbol=Symbol("BTC/USDT", Exchange("BINANCE")),
            order_side=OrderSide.BUY,
            fill_qty=Quantity("0.561000"),
            cum_qty=Quantity("0.561000"),
            leaves_qty=Quantity(0),
            fill_price=Price("15600.12445"),
            currency=USDT,
            is_inverse=False,
            commission=Money("12.20000000", USDT),
            liquidity_side=LiquiditySide.MAKER,
            execution_time=UNIX_EPOCH,
            event_id=uuid,
            event_timestamp=UNIX_EPOCH,
        )

        # Act
        self.assertEqual(f"OrderFilled(account_id=SIM-000, cl_ord_id=O-2020872378423, "
                         f"order_id=123456, position_id=2, strategy_id=SCALPER-001, "
                         f"symbol=BTC/USDT.BINANCE, side=BUY-MAKER, fill_qty=0.561000, "
                         f"fill_price=15600.12445 USDT, cum_qty=0.561000, leaves_qty=0, "
                         f"commission=12.20000000 USDT, id={uuid})", str(event))  # noqa
        self.assertEqual(f"OrderFilled(account_id=SIM-000, cl_ord_id=O-2020872378423, "
                         f"order_id=123456, position_id=2, strategy_id=SCALPER-001, "
                         f"symbol=BTC/USDT.BINANCE, side=BUY-MAKER, fill_qty=0.561000, "
                         f"fill_price=15600.12445 USDT, cum_qty=0.561000, leaves_qty=0, "
                         f"commission=12.20000000 USDT, id={uuid})", repr(event))  # noqa
