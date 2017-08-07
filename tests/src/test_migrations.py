import io

import pytest
from django.core.management import call_command


@pytest.mark.django_db
def test_makemigrations():
    out = io.StringIO()
    call_command('makemigrations', dry_run=True, noinput=True, stdout=out)
    output = out.getvalue()
    assert output == 'No changes detected\n', (
        "`makemigrations` thinks there are schema changes without migrations")