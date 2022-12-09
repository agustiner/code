import os

import acts
import acts.examples

detector, trackingGeometry, contextDecorators  = acts.examples.GenericDetector.create()
s = acts.examples.Sequencer(events=10)

rnd = acts.examples.RandomNumbers(seed=42)

nav = acts.Navigator(trackingGeometry=trackingGeometry)

field = acts.ConstantBField(acts.Vector3(0, 0, 2 * acts.UnitConstants.T))
stepper = acts.EigenStepper(field)

prop = acts.examples.ConcretePropagator(acts.Propagator(stepper, nav))

alg = acts.examples.PropagationAlgorithm(
    propagatorImpl=prop,
    level=acts.logging.INFO,
    randomNumberSvc=rnd,
    ntests=1000,
    sterileLogger=False,
    propagationStepCollection="propagation-steps",
)

s.addAlgorithm(alg)

outputDir = "."
objDir = outputDir + "/obj"
if not os.path.exists(objDir):
   os.mkdir(objDir)

s.addWriter(
    acts.examples.ObjPropagationStepsWriter(
        level=acts.logging.INFO,
        collection="propagation-steps",
        outputDir=objDir,
    )
)

s.addWriter(
    acts.examples.RootPropagationStepsWriter(
        level=acts.logging.INFO,
        collection="propagation-steps",
        filePath=outputDir + "/propagation_steps.root",
    )
)

s.run()

