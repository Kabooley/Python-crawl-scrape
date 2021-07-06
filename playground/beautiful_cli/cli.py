# cli.py
# 
# requirement: `pip install -U click`
import click

@click.command()
@click.argument('name')
@click.option('--greeting', '-g')
def main(name, greeting):
    click.echo("{}, {}".format(greeting, name))

if __name__ == "__main__":
    main()