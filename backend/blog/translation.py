from modeltranslation.translator import translator, TranslationOptions
from .models import Region, District, Service, Worker, Restaurant


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


translator.register(Region, RegionTranslationOptions)
translator.register(District, DistrictTranslationOptions)
translator.register(Service, ServiceTranslationOptions)
translator.register(Worker, WorkerTranslationOptions)
translator.register(Restaurant, RestaurantTranslationOptions)
