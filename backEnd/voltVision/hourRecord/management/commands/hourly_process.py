from django.core.management.base import BaseCommand
from django.utils import timezone
from hourRecord.models import HourRecord
from allData.models import AllData
from datetime import timedelta


class Command(BaseCommand):
    help = 'Processes hourly data and records it'

    def handle(self, *args, **kwargs):
        print("print")
        now = timezone.now()
        one_hour_ago = now - timedelta(hours=1)

        data = AllData.objects.filter(time_date__range=(one_hour_ago, now))

        if not data.exists():
            return

        unit_id = data.first().unit_id
        total_watt = sum(d.volt * d.amp for d in data)

        on_periods = []
        off_periods = []
        current_period = None
        longest_on_period = {'start': None, 'end': None, 'duration': 0}
        longest_off_period = {'start': None, 'end': None, 'duration': 0}

        for record in data:
            if record.amp > 0:  # Consider amp > 0 as 'on'
                if current_period is None:
                    current_period = {'start': record.time_date, 'end': record.time_date}
                else:
                    current_period['end'] = record.time_date
            else:
                if current_period:
                    on_periods.append(current_period)
                    current_period = None
                if off_periods and (record.time_date - off_periods[-1]['end']).total_seconds() < 3600:
                    off_periods[-1]['end'] = record.time_date
                else:
                    off_periods.append({'start': record.time_date, 'end': record.time_date})

        if current_period:
            on_periods.append(current_period)

        for period in on_periods:
            duration = (period['end'] - period['start']).total_seconds()
            if duration > longest_on_period['duration']:
                longest_on_period = {'start': period['start'], 'end': period['end'], 'duration': duration}

        for period in off_periods:
            duration = (period['end'] - period['start']).total_seconds()
            if duration > longest_off_period['duration']:
                longest_off_period = {'start': period['start'], 'end': period['end'], 'duration': duration}

        on_duration = sum((period['end'] - period['start']).total_seconds() / 3600 for period in on_periods)
        off_duration = sum((period['end'] - period['start']).total_seconds() / 3600 for period in off_periods)

        record = HourRecord(
            unit_id=unit_id,
            off_start=longest_off_period['start'],
            off_end=longest_off_period['end'],
            off_duration=off_duration,
            on_start=longest_on_period['start'],
            on_end=longest_on_period['end'],
            on_duration=on_duration,
            watt=total_watt
        )
        record.save()
        print(record)