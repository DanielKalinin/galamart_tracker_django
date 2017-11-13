from django.db import models
import csv


class Area(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return '{} {}'.format(self.id, self.name)


class City(models.Model):
    name = models.CharField(max_length=255)
    area = models.ForeignKey(Area)

    def __str__(self):
        return '{} {} {}'.format(self.id, self.name, self.area)

def load_areas_cities(areas, cities):
    """
    areas - file name of areas in scv format
    cities - file name of cities in scv format
    """
    with open(areas, newline='') as csvfile:
        areas = csv.reader(csvfile, delimiter=',', quotechar='\n')
        areas = [(int(area[0].strip('"')), area[1].strip('"')) for area in areas]
        for area in areas:
            Area.objects.create(id=area[0], name=area[1])
    with open(cities, newline='') as csvfile:
        cities = csv.reader(csvfile, delimiter=',', quotechar='\n')
        cities = [(int(city[0].strip('"')), city[1].strip('"'), int(city[2].strip('"'))) for city in cities]
        for city in cities:
            try:
                City.objects.create(id=city[0], name=city[1], area=Area.objects.get(id=city[2]))
            except:
                pass
