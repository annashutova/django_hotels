import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import hotels_app.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Amenity',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=40, unique=True, verbose_name='title')),
            ],
            options={
                'verbose_name': 'amenity',
                'verbose_name_plural': 'amenities',
                'db_table': 'amenity',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('phone', models.CharField(max_length=11, verbose_name='phone')),
                ('date_of_birth', models.DateField(blank=True, null=True, validators=[hotels_app.models.validate_birth])),
            ],
            options={
                'verbose_name': 'client',
                'verbose_name_plural': 'clients',
                'db_table': 'client',
            },
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('company', models.CharField(blank=True, max_length=40, null=True, verbose_name='company')),
                ('name', models.CharField(max_length=40, verbose_name='name')),
                ('star_rating', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(5)], verbose_name='star rating')),
                ('country', models.CharField(max_length=40, verbose_name='country')),
                ('state', models.CharField(blank=True, max_length=40, null=True, verbose_name='state')),
                ('city', models.CharField(max_length=40, verbose_name='city')),
                ('street', models.CharField(max_length=40, verbose_name='street')),
                ('building', models.CharField(max_length=5, verbose_name='building')),
                ('latitude', models.FloatField(validators=[django.core.validators.MinValueValidator(-90), django.core.validators.MaxValueValidator(90)], verbose_name='latitude')),
                ('longitude', models.FloatField(validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)], verbose_name='longitude')),
            ],
            options={
                'verbose_name': 'hotel',
                'verbose_name_plural': 'hotels',
                'db_table': 'hotel',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('Standart', 'Standart'), ('Superior', 'Superior'), ('Suite', 'Suite'), ('Family room', 'Family room'), ('Deluxe', 'Deluxe'), ('Apartments', 'Apartments'), ('Studio', 'Studio'), ('Duplex', 'Duplex'), ('Business room', 'Business room'), ('Royal suite', 'Royal suite')], max_length=40, verbose_name='type')),
                ('code', models.CharField(max_length=40, verbose_name='code')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(1)], verbose_name='price')),
                ('capacity', models.PositiveSmallIntegerField(verbose_name='capacity')),
                ('double_bed', models.PositiveSmallIntegerField(verbose_name='double bed')),
                ('single_bed', models.PositiveSmallIntegerField(verbose_name='single bed')),
                ('safe', models.BooleanField(blank=True, default=False, null=True, verbose_name='safe')),
                ('tv', models.BooleanField(blank=True, default=False, null=True, verbose_name='tv')),
                ('soundproofing', models.BooleanField(blank=True, default=False, null=True, verbose_name='soundproofing')),
                ('telephone', models.BooleanField(blank=True, default=False, null=True, verbose_name='telephone')),
                ('heating', models.BooleanField(blank=True, default=False, null=True, verbose_name='heating')),
                ('wardrobe', models.BooleanField(blank=True, default=False, null=True, verbose_name='wardrobe')),
                ('shower', models.BooleanField(blank=True, default=False, null=True, verbose_name='shower')),
                ('minibar', models.BooleanField(blank=True, default=False, null=True, verbose_name='minibar')),
                ('air_conditioning', models.BooleanField(blank=True, default=False, null=True, verbose_name='air conditioning')),
                ('bath', models.BooleanField(blank=True, default=False, null=True, verbose_name='bath')),
                ('desk', models.BooleanField(blank=True, default=False, null=True, verbose_name='desk')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotels_app.hotel')),
            ],
            options={
                'verbose_name': 'room',
                'verbose_name_plural': 'rooms',
                'db_table': 'room',
            },
        ),
        migrations.CreateModel(
            name='HotelAmenity',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='price')),
                ('amenity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotels_app.amenity')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotels_app.hotel')),
            ],
            options={
                'verbose_name': 'hotel amenity',
                'verbose_name_plural': 'hotel amenities',
                'db_table': 'hotel_amenity',
            },
        ),
        migrations.AddField(
            model_name='hotel',
            name='amenities',
            field=models.ManyToManyField(through='hotels_app.HotelAmenity', to='hotels_app.amenity', verbose_name='amenities'),
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('check_in', models.DateField(default=datetime.date.today, verbose_name='check_in')),
                ('check_out', models.DateField(default=hotels_app.models.get_checkout_date, verbose_name='check_out')),
                ('status', models.CharField(blank=True, choices=[('Booked', 'Booked'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')], default='Booked', max_length=10)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(1)], verbose_name='price')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotels_app.client')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotels_app.room')),
            ],
            options={
                'verbose_name': 'booking',
                'verbose_name_plural': 'bookings',
                'db_table': 'booking',
                'ordering': ['-check_in', '-check_out'],
            },
        ),
        migrations.AddField(
            model_name='amenity',
            name='hotels',
            field=models.ManyToManyField(through='hotels_app.HotelAmenity', to='hotels_app.hotel', verbose_name='hotels'),
        ),
        migrations.AddConstraint(
            model_name='room',
            constraint=models.CheckConstraint(check=models.Q(('price__gte', 0)), name='room_price_check'),
        ),
        migrations.AddConstraint(
            model_name='room',
            constraint=models.CheckConstraint(check=models.Q(('capacity__gt', 0)), name='capacity_check'),
        ),
        migrations.AddConstraint(
            model_name='room',
            constraint=models.CheckConstraint(check=models.Q(('double_bed__gte', 0)), name='double_bed_check'),
        ),
        migrations.AddConstraint(
            model_name='room',
            constraint=models.CheckConstraint(check=models.Q(('single_bed__gte', 0)), name='single_bed_check'),
        ),
        migrations.AlterUniqueTogether(
            name='room',
            unique_together={('hotel', 'code')},
        ),
        migrations.AddConstraint(
            model_name='hotelamenity',
            constraint=models.CheckConstraint(check=models.Q(('price__gte', 0)), name='amenity_price_check'),
        ),
        migrations.AlterUniqueTogether(
            name='hotelamenity',
            unique_together={('hotel', 'amenity')},
        ),
        migrations.AddIndex(
            model_name='hotel',
            index=models.Index(fields=['name'], name='hotel_name_idx'),
        ),
        migrations.AddConstraint(
            model_name='hotel',
            constraint=models.CheckConstraint(check=models.Q(('star_rating__gte', 0), ('star_rating__lte', 5)), name='star_rate_check'),
        ),
        migrations.AddConstraint(
            model_name='hotel',
            constraint=models.CheckConstraint(check=models.Q(('latitude__gte', -90), ('latitude__lte', 90)), name='latitude_check'),
        ),
        migrations.AddConstraint(
            model_name='hotel',
            constraint=models.CheckConstraint(check=models.Q(('longitude__gte', -180), ('longitude__lte', 180)), name='longitude_check'),
        ),
        migrations.AlterUniqueTogether(
            name='booking',
            unique_together={('check_in', 'check_out', 'room')},
        ),
    ]
