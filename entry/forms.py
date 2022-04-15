from django import forms

class PrototypeForm(forms.Form):
    OPTIONS = (
            ("ABC6", "ABC6"),
            ("ABC","ABC"),
            ("ABC8","ABC8"),
            ("AB6C6","AB6C6"),
            ("AB2C4","AB2C4"),
            ("A2B3C3","A2B3C3"),
            ("AB6C12","AB6C12"),
            ("A3B4C6","A3B4C6"),
            ("AB6C8","AB6C8"),
            ("A3B3C4","A3B3C4"),
            ("AB3C12","AB3C12"),
            ("A3B8C12","A3B8C12"),
            ("AB4C4","AB4C4"),
            ("AB2C2","AB2C2"),
            ("A3B6C8","A3B6C8"),
            ("ABCD6","ABCD6"),
            ("ABC6D6","ABC6D6"),
            ("ABC16","ABC16"),
            ("AB3C8","AB3C8"),
            ("AB4C8","AB4C8"),
            ("ABC2","ABC2"),
            ("AB8C12","AB8C12"),
            ("ABC3","ABC3"),
            ("AB3C6","AB3C6"),
            ("AB2C12","AB2C12"),
            ("AB3C3","AB3C3"),
            ("AB2C3","AB2C3"),
            ("ABC4","ABC4"),
            ("AB12C12","AB12C12"),
            ("A2B3C12","A2B3C12"),
            ("AB3C4","AB3C4"),
            ("A2B2C3","A2B2C3"),
            ("AB2C8","AB2C8"),
            ("A2B3C6","A2B3C6")
        )
    prototypes = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=OPTIONS)

class SpacegroupView(forms.Form):
    OPTIONS = (
            ('216', '216'),
            ('221', '221'),
            ('225', '225'),
            ('227', '227'),
            ('129', '129'),
            ('139', '139'),
            ('140', '140'),
            ('141', '141'),
            ('148', '148'),
            ('164', '164'),
            ('166', '166'),
            ('167', '167'),
            ('186', '186'),
            ('59', '59'),
            ('62', '62'),
            ('63', '63'),
            ('191', '191'),
            ('65', '65'),
            ('194', '194'),
            ('69', '69'),
            ('71', '71'),
            ('74', '74'),
            ('200', '200'),
            ('122', '122'),
            ('123', '123'),

        )

    spacegroups = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=OPTIONS)