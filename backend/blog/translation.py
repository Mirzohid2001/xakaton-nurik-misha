from modeltranslation.translator import translator, TranslationOptions
<<<<<<< HEAD
from .models import Region, District, Service, Worker, Restaurant, Notification, Table, Booking, Payment, Review, \
    BonusPoint, Location, Article, SupportTicket, SupportResponse, Cashback, ServiceUsageStatistic
=======
from .models import Region, District, Service, Worker, Restaurant
>>>>>>> 2b8606c2c895592ee53b23c08b705f894bc271f6


class RegionTranslationOptions(TranslationOptions):
    fields = ('name',)


class DistrictTranslationOptions(TranslationOptions):
    fields = ('name',)


class ServiceTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


class WorkerTranslationOptions(TranslationOptions):
    fields = ('name',)


class RestaurantTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


<<<<<<< HEAD
class NotificationTranslationOptions(TranslationOptions):
    fields = ('message',)


class TableTranslationOptions(TranslationOptions):
    fields = ('image',)


class BookingTranslationOptions(TranslationOptions):
    fields = ('status',)


class PaymentTranslationOptions(TranslationOptions):
    fields = ('payment_method', 'status')


class ReviewTranslationOptions(TranslationOptions):
    fields = ('comment',)


class BonusPointTranslationOptions(TranslationOptions):
    fields = ('reason',)


class LocationTranslationOptions(TranslationOptions):
    fields = ()


class ArticleTranslationOptions(TranslationOptions):
    fields = ('title', 'content')


class SupportTicketTranslationOptions(TranslationOptions):
    fields = ('category', 'subject', 'description', 'status')


class SupportResponseTranslationOptions(TranslationOptions):
    fields = ('message',)


class CashbackTranslationOptions(TranslationOptions):
    fields = ('description',)


class ServiceUsageStatisticTranslationOptions(TranslationOptions):
    fields = ()


=======
>>>>>>> 2b8606c2c895592ee53b23c08b705f894bc271f6
translator.register(Region, RegionTranslationOptions)
translator.register(District, DistrictTranslationOptions)
translator.register(Service, ServiceTranslationOptions)
translator.register(Worker, WorkerTranslationOptions)
translator.register(Restaurant, RestaurantTranslationOptions)
<<<<<<< HEAD
translator.register(Notification, NotificationTranslationOptions)
translator.register(Table, TableTranslationOptions)
translator.register(Booking, BookingTranslationOptions)
translator.register(Review, ReviewTranslationOptions)
translator.register(BonusPoint, BonusPointTranslationOptions)
translator.register(Location, LocationTranslationOptions)
translator.register(Article, ArticleTranslationOptions)
translator.register(SupportTicket, SupportTicketTranslationOptions)
translator.register(SupportResponse, SupportResponseTranslationOptions)
translator.register(Cashback, CashbackTranslationOptions)
translator.register(ServiceUsageStatistic, ServiceUsageStatisticTranslationOptions)
=======
>>>>>>> 2b8606c2c895592ee53b23c08b705f894bc271f6
