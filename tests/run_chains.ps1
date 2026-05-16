$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::InputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)

$RepoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Python = Join-Path $RepoRoot "venv\Scripts\python.exe"
$LightMain = Join-Path $RepoRoot "light_main.py"
$OutFile = Join-Path $RepoRoot "tests\last_tests.txt"

$log = [System.Collections.Generic.List[string]]::new()

function Get-Answers {
    param([string[]]$Output)

    $answers = [System.Collections.Generic.List[string]]::new()
    $current = $null

    foreach ($line in $Output) {
        if ($line -match '^You> Dify> (.*)$') {
            if ($null -ne $current) {
                $answers.Add(($current -join "`n").Trim())
            }
            $current = [System.Collections.Generic.List[string]]::new()
            $current.Add($Matches[1])
        } elseif ($line -match '^You> Bye\.$') {
            if ($null -ne $current) {
                $answers.Add(($current -join "`n").Trim())
                $current = $null
            }
        } elseif ($line -match '^(Loaded environment|Dify base URL|Light mode|Enter text)') {
            continue
        } elseif ($null -ne $current) {
            $current.Add($line)
        }
    }

    if ($null -ne $current) {
        $answers.Add(($current -join "`n").Trim())
    }

    return @($answers.ToArray())
}

function Add-Dialogue {
    param(
        [string]$Title,
        [string[]]$Messages
    )

    $log.Add("# $Title")
    $output = @($Messages | & $Python $LightMain)
    $answers = @(Get-Answers $output)
    $queryMessages = @($Messages | Where-Object { $_ -ne 'EXIT' })

    for ($i = 0; $i -lt $queryMessages.Count; $i++) {
        $log.Add("You> $($queryMessages[$i])")
        $answer = if ($i -lt $answers.Count) { $answers[$i] } else { '<no answer captured>' }
        $answerLines = @($answer -split "`n", 2)
        $log.Add("Dify> $($answerLines[0])")
        if ($answerLines.Count -gt 1) {
            $log.Add($answerLines[1])
        }
    }

    $log.Add('')
}

Add-Dialogue '0. Version check' @('Какая текущая версия?', 'EXIT')
Add-Dialogue '1. Первое сообщение / приветствие' @('Привет', 'EXIT')
Add-Dialogue '1b. Первое сообщение без экзамена' @('Как к вам записаться?', 'EXIT')
Add-Dialogue '2. Только экзамен' @('Здравствуйте, нужна подготовка к ЕГЭ', 'EXIT')
Add-Dialogue '2b. Экзамен и предмет' @('Нужна подготовка к ОГЭ по обществознанию', 'EXIT')
Add-Dialogue '2c. Первое сообщение с приветствием, экзаменом и предметом' @('Здравствуйте, нужна подготовка к ОГЭ по обществознанию', 'EXIT')
Add-Dialogue '3. 5-8 класс, не математика' @('Нужен русский язык 6 класс', 'EXIT')
Add-Dialogue '4. Не ЕГЭ/ОГЭ и не 5-8' @('Нужна подготовка к английскому', 'EXIT')
Add-Dialogue '5. Математика 5-8 -> да -> детали' @('Нужна математика 7 класс', 'да', '500 рублей, два раза в неделю', 'EXIT')
Add-Dialogue '5b. Математика 5-8 -> нет' @('Нужна математика 7 класс', 'нет', 'EXIT')
Add-Dialogue '6. Цена без экзамена и предмета' @('Покажи цены на занятия', 'EXIT')
Add-Dialogue '7. Цена -> только экзамен' @('Покажи цены на занятия', 'ЕГЭ', 'EXIT')
Add-Dialogue '8. Цена -> экзамен и предмет по шагам' @('Покажи цены на занятия', 'ЕГЭ', 'история', 'EXIT')
Add-Dialogue '8b. Цена полным запросом' @('Сколько стоит ЕГЭ история', 'EXIT')
Add-Dialogue '8c. Цена ОГЭ обществознание' @('Цена ОГЭ обществознание', 'EXIT')

$log.Add('# 9-12. Post-price trial/VK flow')
$log.Add('Не прогоняется автоматически в живом Dify, пока knowledge base не возвращает релевантную цену. Эти ветки достижимы только после успешного ответа с ценой.')
$log.Add('')

Add-Dialogue '14. FAQ platform' @('Через какую платформу вы работаете?', 'EXIT')
Add-Dialogue '14b. FAQ format' @('Это индивидуальные уроки?', 'EXIT')
Add-Dialogue '14c. FAQ payment' @('Как оплачивать?', 'EXIT')
Add-Dialogue '14d. FAQ VK' @('У меня нет страницы в ВК, можно в WhatsApp?', 'EXIT')

$log | Set-Content -Path $OutFile -Encoding UTF8
Get-Content $OutFile -Encoding UTF8
