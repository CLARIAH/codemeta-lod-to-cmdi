# -*- coding: utf-8 -*-
import json
import makeCmdi as mc
import pprint as pp
import sys
import unittest

class TestList(unittest.TestCase):

    def test_list(self):
        test_data = '''{ 
    "skos:inScheme": [
        {
            "dct:creator": "Jason Beman"
        },
        {
            "dct:creator": "Jason Antman"
        }
    ]
}
'''
#        stderr(test_data)
        invoer = json.loads(test_data)
        res,attrs = mc.getComponents('tag',invoer,debug=False)
#        stderr(f'attrs: {attrs}')
#        stderr(f'res:\n{res}')
        expected_result = '''        <cmdp:tag>
            <cmdp:inScheme org="skos:inScheme">
                <cmdp:creator org="dct:creator">Jason Beman</cmdp:creator>
            </cmdp:inScheme>
            <cmdp:inScheme org="skos:inScheme">
                <cmdp:creator org="dct:creator">Jason Antman</cmdp:creator>
            </cmdp:inScheme>
        </cmdp:tag>
'''
#        stderr(f'expected:\n{expected_result}')
        self.assertEqual(res,expected_result)

    def test_mixed_content(self):
        test_data = '''{
"developmentStatus": [
                    "trl:Level8Complete",
                {
                    "@id": "https://www.repostatus.org/#active",
                    "@type": "skos:Concept",
                    "og:image": "https://www.repostatus.org/badges/latest/active.svg",
                    "skos:definition": "The project has reached a stable, usable state and is being actively developed.",
                    "skos:inScheme": [
                        {
                            "@id": "https://www.repostatus.org",
                            "@type": "skos:ConceptScheme",
                            "dct:creator": "Jason Antman",
                            "dct:title": "repostatus.org"
                        }
                    ],
                    "skos:prefLabel": "Active"
                }
            ]
}
'''
        expected_result_possible_solution = '''        <cmdp:tag>
            <cmdp:developmentStatus>
                <cmdp:this>trl:Level8Complete</cmdp:this>
            </cmdp:developmentStatus>
            <cmdp:developmentStatus>
                <cmdp:image org="og:image">https://www.repostatus.org/badges/latest/active.svg</cmdp:image>
                <cmdp:definition org="skos:definition">The project has reached a stable, usable state and is being actively developed.</cmdp:definition>
                <cmdp:inScheme org="skos:inScheme">
                    <cmdp:creator org="dct:creator">Jason Antman</cmdp:creator>
                    <cmdp:title org="dct:title">repostatus.org</cmdp:title>
                </cmdp:inScheme>
                <cmdp:prefLabel org="skos:prefLabel">Active</cmdp:prefLabel>
            </cmdp:developmentStatus>
        </cmdp:tag>
'''
        invoer = json.loads(test_data)
        res,attrs = mc.getComponents('tag',invoer,debug=False)
#        stderr(f'res: {res}')
        self.maxDiff = None
        self.assertNotEqual(res,expected_result_possible_solution)

        expected_result_current = '''        <cmdp:tag>
            <cmdp:developmentStatus>trl:Level8Complete</cmdp:developmentStatus>
            <cmdp:developmentStatus>
                <cmdp:image org="og:image">https://www.repostatus.org/badges/latest/active.svg</cmdp:image>
                <cmdp:definition org="skos:definition">The project has reached a stable, usable state and is being actively developed.</cmdp:definition>
                <cmdp:inScheme org="skos:inScheme">
                    <cmdp:creator org="dct:creator">Jason Antman</cmdp:creator>
                    <cmdp:title org="dct:title">repostatus.org</cmdp:title>
                </cmdp:inScheme>
                <cmdp:prefLabel org="skos:prefLabel">Active</cmdp:prefLabel>
            </cmdp:developmentStatus>
        </cmdp:tag>
'''
        self.assertEqual(res,expected_result_current)


    def test_empty_type(self):
        test_data = '''{
        "@type": {
                    "@id": "skos:Concept",
                    "@type": "owl:Class"
                }
}
'''
        expected_result = ''
        invoer = json.loads(test_data)
        res,attrs = mc.getComponents('tag',invoer,debug=False)
        self.assertEqual(res,expected_result)


def stderr(text,nl='\n'):
    sys.stderr.write(f"{text}{nl}")


if __name__ == '__main__':
    unittest.main()

