
Installing RabitMQ on Ubuntu:

Go to:

http://www.rabbitmq.com/install-debian.html

See the section on adding the repository, and follow those instructions

We will be using the management API for the exercise:

[A link to the latest API documentation](https://www.rabbitmq.com/management.html#http-api)

If you are using shell scripts for management, I suggest something like jq to convert things into
simple lists. Your shell-foo is still going to have to be pretty good...

[jQ documentation](https://stedolan.github.io/jq/)

You can install jq in Ubuntu with apt-get:

  $ sudo apt-get install jq
