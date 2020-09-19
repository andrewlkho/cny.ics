#!/usr/bin/env python3

import datetime
import lunardate


def get_animal(year):
    """Get the presiding animal zodiac for a given year."""
    animals = [
        "Rat",
        "Ox",
        "Tiger",
        "Rabbit",
        "Dragon",
        "Snake",
        "Horse",
        "Goat",
        "Monkey",
        "Rooster",
        "Dog",
        "Pig",
    ]
    return animals[(year - 1900) % len(animals)]


def cny_gregorian(year):
    """Get the date in the Gregorian calendar of CNY for a given year."""
    if year < 1900 or year > 2099:
        raise ValueError(
            "Year {} is outside the scope of lunardate (1900-2099)".format(year)
        )

    return lunardate.LunarDate(year, 1, 1).toSolarDate()


def gen_ical_vevent(year):
    """Generate an iCalendar object representing CNY for a given year."""
    vevent = "\r\n".join(
        [
            "BEGIN:VEVENT",
            "DTSTAMP:{}".format(datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")),
            "UID:{}@github.com/andrewlkho/cny.ics".format(year),
            "DTSTART;VALUE=DATE:{}".format(cny_gregorian(year).strftime("%Y%m%d")),
            "DTEND;VALUE=DATE:{}".format(
                (cny_gregorian(year) + datetime.timedelta(days=1)).strftime("%Y%m%d")
            ),
            "SUMMARY;LANGUAGE=en-GB:Chinese New Year",
            "DESCRIPTION;LANGUAGE=en-GB:Year of the {}".format(get_animal(year)),
            "END:VEVENT",
        ]
    )
    return vevent


def main():
    vcal_header = "\r\n".join(
        [
            "BEGIN:VCALENDAR",
            "PRODID:-//andrewlkho//cny.ics//EN",
            "VERSION:2.0",
            "CALSCALE:GREGORIAN",
        ]
    )
    vcal_body = "\r\n".join([gen_ical_vevent(year) for year in range(1900, 2100)])
    vcal_footer = "END:VCALENDAR"
    vcal = "\r\n".join([vcal_header, vcal_body, vcal_footer])

    print(vcal)


if __name__ == "__main__":
    main()
