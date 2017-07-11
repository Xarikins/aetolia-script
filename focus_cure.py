from curing_balance import CuringBalance

class FocusCure(CuringBalance):

    def __init__(self, mud):
        super(FocusCure, self).__init__(mud, 
                name="Focus",
                fire_trigger="^You focus your mind intently on curing your mental maladies\.$",
                busy_trigger="^You concentrate, but your mind is too tired to focus\.$",
                reset_trigger="^Your mind is able to focus once again\.$",
                command="focus"
                )
