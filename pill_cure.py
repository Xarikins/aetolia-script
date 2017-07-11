from curing_balance import CuringBalance

class PillCure(CuringBalance):

    def __init__(self, mud):
        super(PillCure, self).__init__(mud, 
                name="Pill",
                fire_trigger="^You swallow a .+ pill\.$",
                busy_trigger="^You cannot swallow another pill right now\.$",
                reset_trigger="^You may swallow another pill\.$",
                command="eat %s"
                )
