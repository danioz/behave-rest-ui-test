from dataclasses import dataclass
from typing import Optional


@dataclass
class BookingDataModel:
    bookingid: Optional[int]
    booking: 'Booking'

    @dataclass
    class Booking:
        firstname: str
        lastname: str
        totalprice: int
        depositpaid: bool
        bookingdates: 'BookingDates'
        additionalneeds: str

    @dataclass
    class BookingDates:
        checkin: str
        checkout: str