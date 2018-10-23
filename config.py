from decouple import Csv, config


TOKEN = config('TOKEN')
WEBHOOK = config('WEBHOOK', default=False, cast=bool)
ALLOWED_CHANNELS = config('ALLOWED_CHANNELS', default='', cast=Csv())
SENTRY_DSN = config('SENTRY_DSN', default=None)
SENTRY_ENVIRONMENT = config('SENTRY_ENVIRONMENT', default='dev')
HANDLER = config('HANDLER', default=None)
REGEX = config('REGEX', default=None)
