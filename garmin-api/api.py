import json

API_HOST = 'https://apis.garmin.com/'

class ApiClient:
    def garmin_process_push_or_ping_item(self, item):
        extract_fields = ['summaryId', 'startTimeInSeconds', 'callbackURL', 'fileType', 'userId', 'userAccessToken']

        # row:API相關資料 data:PUSH進來的資料
        row = {}
        data = {}
        for (key, val) in item.items():
            if key in extract_fields:
                row[key] = val
            else:
                data[key] = val

        if 'callbackURL' in row:
            isping = True
        else:
            isping = False
            row['json'] = json.dumps(data)

        return row