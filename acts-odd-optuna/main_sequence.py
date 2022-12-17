# in
# n_max_seeds_per_sp_m number of compatible 
# cot_theta_max cot of maximum theta angle
# sigmaScattering How many sigmas of scattering to include in seeds
# radLengthPerSeed Average Radiation Length
# impactMax max impact parameter in mm
# maxPtScattering maximum Pt for scattering cut in GeV
# deltaRMin minimum value for deltaR separation in mm
# deltaRMax maximum value for deltaR separation in mm
# out
# some cool fucking shit


from acts.examples.reconstruction import (
    addSeeding,
    TruthSeedRanges,
    ParticleSmearingSigmas,
    SeedfinderConfigArg,
    SeedingAlgorithm,
    TrackParamsEstimationConfig,
    CKFPerformanceConfig,
    addCKFTracks,
)
    
import pathlib, acts, acts.examples
import acts.examples.simulation
from acts.examples.simulation import (
    MomentumConfig,
    EtaConfig,
    ParticleConfig,
    ParticleSelectorConfig,
)
from acts.examples.reconstruction import (
    TruthSeedRanges,
    CKFPerformanceConfig,
    VertexFinder,
    TrackSelectorRanges,
)
from acts.examples.simulation import (
    addParticleGun,
    EtaConfig,
    PhiConfig,
    ParticleConfig,
    addFatras,
    addDigitization,
)    
from acts.examples.odd import getOpenDataDetector
import datetime
import os

def getActsSourcePath():
    return pathlib.Path("/home/user1/code/acts/source")

def getOpenDataDetectorPath():
    return getActsSourcePath() / "thirdparty" / "OpenDataDetector"

def run(maxSeedsPerSpM,
        cotThetaMax,
        sigmaScattering,
        radLengthPerSeed,
        impactMax,
        maxPtScattering,
        deltaRMin,
        deltaRMax,
        ):
    truthSmearedSeeded = False
    truthEstimatedSeeded = False
    logger = acts.logging.getLogger("full_chain_odd")
    logger.info("Starting full_chain_odd")
    u = acts.UnitConstants
    oddPath = getOpenDataDetectorPath()
    outputDir = pathlib.Path.cwd()
    oddMaterialMap = oddPath / "data/odd-material-maps.root"
    oddDigiConfig = oddPath / "config/odd-digi-smearing-config.json"
    oddSeedingSel = oddPath / "config/odd-seeding-config.json"
    oddMaterialDeco = acts.IMaterialDecorator.fromFile(oddMaterialMap)
    
    detector, trackingGeometry, decorators = getOpenDataDetector(
        oddPath, mdecorator=oddMaterialDeco
    )
    field = acts.ConstantBField(acts.Vector3(0.0, 0.0, 2.0 * u.T))
    rnd = acts.examples.RandomNumbers(seed=42)
    
    s = acts.examples.Sequencer(events = 1,
                                numThreads = -1,
                                outputDir = str(outputDir))
    
    acts.examples.simulation.addPythia8(
        s,
        hardProcess=["Top:qqbar2ttbar=on"],
        npileup=10,
        vtxGen=acts.examples.GaussianVertexGenerator(
            stddev=acts.Vector4(0.0125 * u.mm, 0.0125 * u.mm, 55.5 * u.mm, 5.0 * u.ns),
            mean=acts.Vector4(0, 0, 0, 0),
        ),
        rnd=rnd,
        outputDirRoot=outputDir
    )
    
    acts.examples.simulation.addFatras(
        s,
        trackingGeometry,
        field,
        outputDirRoot=outputDir,
        rnd=rnd,
    )
    
    acts.examples.simulation.addDigitization(
        s,
        trackingGeometry,
        field,
        digiConfigFile=oddDigiConfig,
        outputDirRoot=outputDir,
        rnd=rnd,
    )
    
    acts.examples.reconstruction.addSeeding(
        s,
        trackingGeometry,
        field,
        TruthSeedRanges(pt=(500.0 * u.MeV, None), nHits=(9, None)),
        ParticleSmearingSigmas(pRel=0.01),
        SeedfinderConfigArg(
            r=(None, 200 * u.mm),
            deltaR=(deltaRMin * u.mm, deltaRMax * u.mm),
            collisionRegion=(-250 * u.mm, 250 * u.mm),
            z=(-2000 * u.mm, 2000 * u.mm),
            maxSeedsPerSpM=maxSeedsPerSpM,
            cotThetaMax=cotThetaMax,
            sigmaScattering=sigmaScattering,
            radLengthPerSeed=radLengthPerSeed,
            maxPtScattering=maxPtScattering * u.GeV,
            minPt=500 * u.MeV,
            bFieldInZ=1.99724 * u.T,
            impactMax=impactMax * u.mm,
        ),
        TrackParamsEstimationConfig(deltaR=(10.0 * u.mm, None)),
        seedingAlgorithm=SeedingAlgorithm.TruthSmeared
        if truthSmearedSeeded
        else SeedingAlgorithm.TruthEstimated
        if truthEstimatedSeeded
        else SeedingAlgorithm.Default,
        geoSelectionConfigFile=oddSeedingSel,
        outputDirRoot=outputDir,
        rnd=rnd,
    )

    acts.examples.reconstruction.addCKFTracks(
        s,
        trackingGeometry,
        field,
        CKFPerformanceConfig(ptMin=1.0 * u.GeV, nMeasurementsMin=6),
        outputDirRoot=outputDir
    )
    
    s.run()
