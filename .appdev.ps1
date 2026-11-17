function Invoke-Pip {
    docker exec $env:APP_NAME pip
}

function Invoke-Python {
    docker exec -w /opt/python $env:APP_NAME python
}

function Invoke-Pytest {
    docker exec -w /opt/python $env:APP_NAME pytest tests
}

Set-Alias -Name pip -Value Invoke-Pip
Set-Alias -Name python -Value Invoke-Python
Set-Alias -Name pytest -Value Invoke-Pytest