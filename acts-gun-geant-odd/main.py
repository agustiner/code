#!/usr/bin/env python3
from pathlib import Path

import acts
import os
import datetime
import acts.examples
from acts.examples.simulation import addParticleGun, addGeant4, EtaConfig, MomentumConfig, ParticleConfig
from acts.examples.odd import getOpenDataDetector
from pathlib import Path

def runGeant4(
    geometryService,
    trackingGeometry,
    field,
    outputDir
):
    s = acts.examples.Sequencer(events=2, numThreads=1)
    s.config.logLevel = acts.logging.INFO
    rnd = acts.examples.RandomNumbers()
    
    addParticleGun(
        s,
        MomentumConfig(1.0 * acts.UnitConstants.GeV, 10.0 * acts.UnitConstants.GeV, True),
        EtaConfig(-2.0, 2.0),
        ParticleConfig(1, acts.PdgParticle.eMuon, True),
        rnd=rnd,
    )

    os.mkdir(outputDir)
    os.mkdir(outputDir / 'geant')
    addGeant4(
        s,
        geometryService,
        trackingGeometry,
        field,
        outputDirRoot = outputDir / 'geant',
        rnd=rnd,
    )

    return s


if "__main__" == __name__:
    
    detector, trackingGeometry, decorators = getOpenDataDetector(
        Path("/home/user1/code/acts/source/thirdparty/OpenDataDetector")
    )
    field = acts.ConstantBField(acts.Vector3(0, 0, 2 * acts.UnitConstants.T))
    
    outputDir = Path.cwd() / datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    runGeant4(detector.geometryService, trackingGeometry, field, outputDir).run()
