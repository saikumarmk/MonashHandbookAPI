from requests import post


class PreReqAPI:
    BASE_URL = "https://mscv.apps.monash.edu"

    def __init__(self) -> None:
        return

    def _post(self, content: dict) -> dict:

        json_content = self._build_post_content(content)
        request = post(self.BASE_URL, json=json_content)

        if request.status_code != 200:
            print(request.reason)
            raise ValueError(
                f'Error code: {request.status_code}\nReason: {request.reason}')

        print(request.elapsed.total_seconds())
        return request.json()

    def _build_post_content(self, units: list[str]) -> dict:

        return {
            "startYear": 2022,
            "advancedStanding": [

            ],
            "internationalStudent": False,
            "courseInfo": {

            },
            "teachingPeriods": [
                {
                    "year": 2022,
                    "code": "S1-01",
                    "units": [
                            {
                                "unitCode": unit_code,
                                "placeholder": False
                            } for unit_code in units
                    ],
                    "intermission": False,
                    "studyAbroad": False
                }
            ]
        }

    def get_unit_reqs(self, units: list[str]) -> dict:
        return self._post(units)


if __name__ == "__main__":

    t = PreReqAPI()
    print(t.get_unit_reqs(['MTH2010']))
    print(t.get_unit_reqs(['MTH1010',
                           'MTH1020',
                           'MTH1030',
                           'MTH1035',
                           'MTH2010',
                           'MTH2019',
                           'MTH2021',
                           'MTH2025',
                           'MTH2121',
                           'MTH2132',
                           'MTH2140',
                           'MTH2222',
                           'MTH3011',
                           'MTH3110',
                           'MTH3121',
                           'MTH3130',
                           'MTH3140',
                           'MTH3241',
                           'MTH3251',
                           'MTH3320',
                           'MTH3330',
                           'MTH3360']))
