from curing_balance import CuringBalance

class SmokeCure(CuringBalance):

    def __init__(self, mud):
        super(SmokeCure, self).__init__(mud, 
                name="Smoke",
                fire_trigger="^You take a long drag off your pipe filled with .+\.$",
                busy_trigger="^You cannot smoke another pipe right now\.$",
                reset_trigger="^You may smoke another herb\.$",
                command="smoke %s"
                )
