# Release note scraper *WIP*

## Goal

Terraform provider releases can sometimes contain breaking changes. I wanted to
build a tool that could send me some kind of notification once a new version is
released and list out any breaking changes (if they exist).

## Solution

The solution is quite basic. A url to the raw markdown changelog file
in git is provided on input. The Python script parses the content to look for
the most recent release and whether or not it contains any breaking changes. If it
does, a message with the breaking changes is sent to a Slack channel.
