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
        )
    prototypes = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=OPTIONS)

class SpacegroupView(forms.Form):
    OPTIONS = (
            ('216', '216'),
            ('221', '221'),
            ('225', '225'),
        )

    spacegroups = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=OPTIONS)