#!/usr/bin/env python3
from pathlib import Path

import acts
import os
import datetime
import acts.examples
from acts.examples.simulation import addParticleGun, addGeant4, EtaConfig, MomentumConfig, ParticleConfig
from acts.examples.odd import getOpenDataDetector
from pathlib import Path

def geant_sequencer():
    s = acts.examples.Sequencer(events=2, logLevel = acts.logging.DEBUG)
    s.config.logLevel = acts.logging.INFO
    rnd = acts.examples.RandomNumbers()
    outputDir = Path.cwd() / datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    os.mkdir(outputDir)

    os.mkdir(outputDir / 'particlegun')
    addParticleGun(
        s,
        MomentumConfig(20.0 * acts.UnitConstants.GeV, 30.0 * acts.UnitConstants.GeV, True),
        ParticleConfig(1, acts.PdgParticle.eElectron, True),
        multiplicity = 7,
        rnd = rnd,
        outputDirRoot = outputDir / 'particlegun',
        printParticles = True
    )

    os.mkdir(outputDir / 'geant')
    detector, trackingGeometry, decorators = getOpenDataDetector(
        Path("/home/user1/code/acts/source/thirdparty/OpenDataDetector")
    )
    field = acts.ConstantBField(acts.Vector3(0, 0, 2 * acts.UnitConstants.T))
    addGeant4(
        s,
        detector.geometryService,
        trackingGeometry,
        field,
        outputDirRoot = outputDir / 'geant',
        rnd=rnd,
    )

    return s


if "__main__" == __name__:
    sequencer = geant_sequencer()
    sequencer.run()
