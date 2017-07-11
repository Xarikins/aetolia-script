from curing_balance import CuringBalance

class TreeCure(CuringBalance):

    def __init__(self, mud):
        super(TreeCure, self).__init__(mud, 
                name="Tree",
                fire_trigger="^You touch the tree of life tattoo\.$",
                busy_trigger="^Your tree of life tattoo glows faintly for a moment then fades, leaving you unchanged\.$",
                reset_trigger="^Your tree tattoo tingles slightly\.$",
                command="touch tree"
                )

