from curing_balance import CuringBalance

class PoulticeCure(CuringBalance):

    def __init__(self, mud):
        super(PoulticeCure, self).__init__(mud, 
                name="Poultice",
                fire_trigger="^You press a mending poultice against your skin, rubbing it into your flesh\.$",
                busy_trigger="^You are not yet able to absorb another poultice\.$",
                reset_trigger="^You are again able to absorb a poultice\.$",
                command="apply %s"
                )
