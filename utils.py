import random
import numpy as np

from random import randint
from monitoring.choices import city_choices
from monitoring.models import Profile, Address, Monitoring
from prediction.models import HealthCenter, HealthCenterStatus


def create_dummy_profiles(count, suspect=False, result='SR', city='Maceió', status='N'):
    for i in range(count):
        profile = Profile.objects.create(full_name='Paciente %d' % random.randrange(1000000),
                                         age=random.randrange(100),
                                         birth_date='1970-01-01'
                                         )
        address = Address.objects.create(profile_id=profile.id, city=city, primary=True)
        monitoring = Monitoring.objects.create(profile_id=profile.id, result=result,
                                               status=status)

def run_profiles(suspect=900, sick=240, hospital=48, icu=12, dead=5, seed=42):
    print("Populando banco de dados com:")
    print(" - %d casos suspeitos" % suspect)
    print(" - %d casos confirmados" % sick)
    print(" - %d casos hospitalizados" % hospital)
    print(" - %d casos em UTI" % icu)
    print(" - %d mortos" % dead)
    data = {
        "suspect": suspect,
        "sick": sick,
        "hospital": hospital,
        "icu": icu,
	"dead": dead
    }

    np.random.seed(seed)
    # random number vector with sum 1
    distribution = np.random.dirichlet(np.ones(len(city_choices)), size=1)[0]
    for i, city in enumerate(city_choices):
        create_dummy_profiles(int(np.ceil(data["suspect"]*distribution[i])), suspect=True, city=city[0])
        create_dummy_profiles(int(np.ceil(data["sick"]*distribution[i])), result="PO", city=city[0])
        create_dummy_profiles(int(np.ceil(data["hospital"]*distribution[i])), result="PO", city=city[0], status="H")
        create_dummy_profiles(int(np.ceil(data["icu"]*distribution[i])), result="PO", city=city[0], status="U")
        create_dummy_profiles(int(np.ceil(data["dead"]*distribution[i])), result="PO", city=city[0], status="M")

    print("Feito.")

def run_health_center_status():
    hcs_to_create=[]

    for hc in HealthCenter.objects.all():
        beds = randint(0, 180)
        occupied_beds = randint(0, beds)
        icus = randint(0, 180)
        occupied_icus = randint(0, icus)
        respirators = randint(0, 180)
        occupied_respirators = randint(0, respirators)

        hcs_to_create.append(HealthCenterStatus(
            health_center=hc,
            beds=beds,
            occupied_beds=occupied_beds,
            icus=icus,
            occupied_icus=occupied_icus,
            respirators=respirators,
            occupied_respirators=occupied_respirators
        ))

    HealthCenterStatus.objects.bulk_create(hcs_to_create)

# https://docs.djangoproject.com/en/3.0/topics/db/sql/#executing-custom-sql-directly
def dictfetchall(cursor):
    '''Returns all rows from a cursor as a dict'''
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
