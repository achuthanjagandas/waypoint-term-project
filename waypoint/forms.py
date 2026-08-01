from django import forms


class TrailReportForm(forms.Form):
    """Collect a visitor's report about current trail conditions."""

    reporter_name = forms.CharField(
        label="Your name",
        max_length=100,
    )
    email = forms.EmailField(
        label="Email address",
    )
    trail_name = forms.CharField(
        label="Trail name",
        max_length=150,
    )
    condition = forms.ChoiceField(
        label="Trail condition",
        choices=[
            ("open", "Open and clear"),
            ("muddy", "Muddy"),
            ("obstructed", "Obstructed"),
            ("closed", "Closed"),
        ],
    )
    comments = forms.CharField(
        label="Additional details",
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 5,
                "placeholder": "Describe anything other hikers should know.",
            }
        ),
    )