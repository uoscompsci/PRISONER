function cls {
osascript -e 'tell application "System Events" to keystroke "k" using command down'
}

cls && nosetests prisoner.workflow -v -x --with-coverage --cover-package=prisoner