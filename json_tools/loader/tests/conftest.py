import os
import pytest
from glob import glob

@pytest.fixture(params=["./sample_json"])
def sample_jsons(request):
    files = [f for f in glob(os.path.join(request.param, "*")) if os.path.isfile(f)]
    return files