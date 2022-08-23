import json
from base_api import BaseAPI


class UnitAPI(BaseAPI):

    def __init__(self) -> None:
        super().__init__()

    def _build_post_content(self, content: str = 'MTH3170', options: dict = None) -> dict:
        return {
            "query": {
                "bool": {
                    "must": [
                        {"query_string": {"query": f"monash2_psubject.code: {content}"}},
                        {"term": {"live": True}},
                    ]
                }
            },
            "aggs": {
                "implementationYear": {
                    "terms": {
                        "field": "monash2_psubject.implementationYear_dotraw",
                        "size": 100
                    }
                },
                "availableInYears": {
                    "terms": {"field": "monash2_psubject.availableInYears_dotraw", "size": 100}
                },
            },
            "size": 100,
            "_source": {
                "includes": ["versionNumber", "availableInYears", "implementationYear"]
            },
        }

    def get_unit(self, unit: str) -> dict:
        search_results = self._post(unit, {})
        return [self._summarise_unit_info(json.loads(result['data']))
                for result in search_results['contentlets']]

    def _summarise_unit_info(self, unit_json: dict) -> dict:
        """

        Returns a filtered down version of unit information.


        """

        return {

            'unit_name': unit_json['title'],
            'unit_code': unit_json['unit_code'],
            'credit_points': unit_json['credit_points'],
            'school': unit_json['school']['value'],
            'workload': unit_json['workload_requirements'],
            'synopsis': unit_json['handbook_synopsis'],
            'learning_outcomes': sorted([(int(item['number']), item['description'])
                                         for item in unit_json["unit_learning_outcomes"]], key=lambda x: x[0]),
            'requisites': unit_json['requisites'],
            'enrolment_rules_group': unit_json['enrolment_rules_group'],
            'location': [location['location']['value'] for location in unit_json['unit_offering']],
            'teaching_periods': [teach['teaching_period']["value"] for teach in unit_json['unit_offering']],
            # add learning_activities_grouped
            # Add teaching_approaches
            'academic_contact_roles': [{
                'role': role['role'],
                'contacts': [
                    {'contact_name': contact['contact_name'],
                     'contact_role':contact['contact_role']['label'],
                     'display_details': contact['display_name']
                     } for contact in role['contacts']
                ]}
                for role in unit_json['academic_contact_roles']
            ]

        }
