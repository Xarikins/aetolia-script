from curing_balance import CuringBalance

class EraseCure(CuringBalance):

    def __init__(self, mud):
        super(EraseCure, self).__init__(mud, 
                name="Erase",
                fire_trigger="^Marshalling your will, you bear down on one of your maladies and brutally wipe it from existence\.$",
                busy_trigger="^You cannot use that skill again so soon\.$",
                reset_trigger="^You feel capable of erasing your maladies once more\.$",
                command="focus"
                )
