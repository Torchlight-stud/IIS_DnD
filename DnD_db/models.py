from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse
from django.utils.timezone import now


class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    nickname = models.CharField(max_length=100, blank=False, default='new player', unique=True)
    session_part = models.OneToOneField('Session', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.nickname

    def get_absolute_url(self):
        return '/player_details/{}'.format(self.id)


class Session(models.Model):
    location = models.CharField(max_length=100, blank=False, default='Location for session')
    creation_date = models.DateTimeField(default=now)
    creator = models.ForeignKey(Player, on_delete=models.CASCADE, blank=False, null=True)
    campaign = models.ForeignKey('Campaign', on_delete=models.SET_NULL, blank=False, null=True)

    def __str__(self):
        return "{}: {}".format(self.pk, self.location)

    def get_absolute_url(self):
        return reverse('detailed_session', kwargs={'id': self.id})


class Character(models.Model):
    HB = 'Hobbit'
    KU = 'Kuduk'
    DW = 'Dwarf'
    EL = 'Elf'
    HM = 'Human'
    BA = 'Barbar'
    KR = 'Kroll'
    RACES = (
        (HB, HB),
        (KU, KU),
        (DW, DW),
        (EL, EL),
        (HM, HM),
        (BA, BA),
        (KR, KR),
    )

    WA = 'Warrior'
    FI = 'Fighter'
    FE = 'Fencer'
    RA = 'Ranger'
    ST = 'Strider'
    DR = 'Druid'
    WI = 'Wizard'
    SO = 'Sorcerer'
    MA = 'Mage'
    AL = 'Alchemist'
    TE = 'Theurg'
    PY = 'Pyrofor'
    TH = 'Thief'
    RO = 'Robber'
    SI = 'Sicco'
    SPECS = (
        (WA, WA),
        (FI, FI),
        (FE, FE),
        (RA, RA),
        (ST, ST),
        (DR, DR),
        (WI, WI),
        (SO, SO),
        (MA, MA),
        (AL, AL),
        (TE, TE),
        (PY, PY),
        (TH, TH),
        (RO, RO),
        (SI, SI),
    )

    name = models.CharField(max_length=100, unique=True, default='New character')
    race = models.CharField(max_length=6, choices=RACES, default=HM)
    speciality = models.CharField(max_length=9, choices=SPECS, default=WA)
    level = models.IntegerField(default=1)
    owner = models.ForeignKey(Player, on_delete=models.CASCADE, blank=False, null=True)
    death = models.OneToOneField('CharacterDeath', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detailed_character', kwargs={'id': self.id})


class Map(models.Model):
    name = models.CharField(max_length=100, default='New map', unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True)
    description = models.TextField(default='Some description')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detailed_map', kwargs={'id': self.id})


class Enemy(models.Model):
    DE = 'Demon'
    DR = 'Dragon'
    SN = 'Snake'
    IN = 'Insect'
    HU = 'Humanoid'
    MA = 'Magical'
    ST = 'Statues'
    CR = 'Creature'
    ENEMIES = (
        (DE, DE),
        (DR, DR),
        (SN, SN),
        (IN, IN),
        (HU, HU),
        (MA, MA),
        (ST, ST),
        (CR, CR),
    )
    name = models.CharField(max_length=100, unique=True, blank=False, default='New enemy')
    type = models.CharField(max_length=8, blank=False, choices=ENEMIES, default=DE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detailed_enemy', kwargs={'id': self.id})


class Adventure(models.Model):
    name = models.CharField(max_length=100, unique=True, default='New adventure')
    difficulty = models.IntegerField(default=0)
    purpose = models.TextField(default='New purpose')
    location = models.CharField(max_length=100, default='Some location')
    map = models.ManyToManyField(Map, blank=False)
    enemies = models.ManyToManyField(Enemy, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detailed_adventure', kwargs={'id': self.id})


class Campaign(models.Model):
    name = models.CharField(max_length=100, unique=True, default='New campaign')
    info = models.TextField(default='Campaign info', blank=False)
    adventures = models.ManyToManyField(Adventure, blank=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detailed_campaign', kwargs={'id': self.id})


# TODO: reference to character
class CharacterDeath(models.Model):
    time = models.DateTimeField(default=now)
    place = models.ForeignKey('Map', on_delete=models.CASCADE, blank=False, null=True)


class Inventory(models.Model):
    WP = 'Weapon'
    AR = 'Armor'
    FO = 'Food'
    PO = 'Potion'
    TO = 'Tool'
    OT = 'Other'

    TYPES = (
        (WP, WP),
        (AR, AR),
        (FO, FO),
        (PO, PO),
        (TO, TO),
        (OT, OT),
    )
    name = models.CharField(max_length=100, default='New item')
    type = models.CharField(max_length=6, blank=False, choices=TYPES, default=WP)
    owner = models.ForeignKey(Character, blank=True, null=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detailed_inventory', kwargs={'id': self.id})

    class Meta:
        unique_together = (('name', 'type'),)


# Common queries
def created_maps(user):
    return False


def created_sessions(user):
    return False
