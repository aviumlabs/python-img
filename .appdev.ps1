function Invoke-Pip {
    docker exec app pip
}

function Invoke-Python {
    docker exec -w /opt/python app python
}

function Invoke-Pytest {
    docker exec -w /opt/python app pytest tests
}

Set-Alias -Name pip -Value Invoke-Pip
Set-Alias -Name python -Value Invoke-Python
Set-Alias -Name pytest -Value Invoke-Pytest