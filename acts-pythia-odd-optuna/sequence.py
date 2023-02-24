# n_max_seeds_per_sp_m number of compatible 
# cot_theta_max cot of maximum theta angle
# sigmaScattering How many sigmas of scattering to include in seeds
# radLengthPerSeed Average Radiation Length. average radiation lengths of material on the length of a seed
# impactMax max impact parameter in mm
# maxPtScattering maximum Pt for scattering cut in GeV
# deltaRMin minimum value for deltaR separation in mm
# deltaRMax maximum value for deltaR separation in mm
# out
# .root file
# .root file
# .root file

import pathlib
import acts
import acts.examples
import acts.examples.simulation
from acts.examples.reconstruction import (
    CKFPerformanceConfig,
    ParticleSmearingSigmas,
    SeedFinderConfigArg,
    SeedFinderOptionsArg,
    SeedingAlgorithm,
    TrackParamsEstimationConfig,
    TrackSelectorRanges,
    TruthSeedRanges,
    VertexFinder,
    addCKFTracks,
    addSeeding,
)    
from acts.examples.simulation import (
    ParticleSelectorConfig,
    addDigitization,
    addFatras
)
from acts.examples.odd import getOpenDataDetector

def getActsSourcePath():
    return pathlib.Path("/home/user1/code/acts/source")

def getOpenDataDetectorPath():
    return getActsSourcePath() / "thirdparty" / "OpenDataDetector"

# Run the Sequence, starting from instantiating events and ending
# with reconstructed tracks. This sequence may be put into an
# optimizer trial function.
# Input
#
# Output
# 
def run(output_path, param_dict):
    logger = acts.logging.getLogger("full_chain_odd")
    logger.info("Starting Sequence")
    truthSmearedSeeded = False
    truthEstimatedSeeded = False
    u = acts.UnitConstants
    oddPath = getOpenDataDetectorPath()
    oddMaterialMap = oddPath / "data/odd-material-maps.root"
    oddDigiConfig = oddPath / "config/odd-digi-smearing-config.json"
    oddSeedingSel = oddPath / "config/odd-seeding-config.json"
    oddMaterialDeco = acts.IMaterialDecorator.fromFile(oddMaterialMap)
    
    detector, trackingGeometry, decorators = getOpenDataDetector(
        oddPath, mdecorator = oddMaterialDeco
    )
    field = acts.ConstantBField(acts.Vector3(0.0, 0.0, 2.0 * u.T))
    rnd = acts.examples.RandomNumbers(seed=42)

    # events: number of collisions to generate. one performance_ckf.root will be made for all 100 events.
    # outputDir: where to output the timing.tsv data
    s = acts.examples.Sequencer(events = 1,
                                outputDir = str(output_path))
    
    acts.examples.simulation.addPythia8(
        s,
        cmsEnergy = 14 * acts.UnitConstants.TeV,
        hardProcess = ["Top:qqbar2ttbar=on"],
        npileup = 100,
        vtxGen = acts.examples.GaussianVertexGenerator(
            stddev = acts.Vector4(0.0125 * u.mm, 0.0125 * u.mm, 55.5 * u.mm, 5.0 * u.ns),
            mean = acts.Vector4(0, 0, 0, 0),
        ),
        rnd = rnd
    )
    
    acts.examples.simulation.addFatras(
        s,
        trackingGeometry,
        field,
        ParticleSelectorConfig(eta = (-3, 3), pt = (150 * u.MeV, None), removeNeutral = True),
        rnd = rnd,
    )
    
    acts.examples.simulation.addDigitization(
        s,
        trackingGeometry,
        field,
        digiConfigFile = oddDigiConfig,
        rnd = rnd,
    )
    
    acts.examples.reconstruction.addSeeding(
        s,
        trackingGeometry,
        field,
        TruthSeedRanges(eta = (-3, 3), pt = (1.0 * u.GeV, None), nHits = (9, None)),        
        ParticleSmearingSigmas(pRel = 0.01),
        SeedFinderConfigArg(
            r=(None, 200 * u.mm),
            deltaR=(param_dict['deltaRMin'] * u.mm, param_dict['deltaRMax'] * u.mm),
            collisionRegion = (-250 * u.mm, 250 * u.mm),
            z=(-2000 * u.mm, 2000 * u.mm),
            maxSeedsPerSpM = param_dict['maxSeedsPerSpM'],
            cotThetaMax = param_dict['cotThetaMax'],
            sigmaScattering = param_dict['sigmaScattering'],
            radLengthPerSeed = param_dict['radLengthPerSeed'],
            maxPtScattering = param_dict['maxPtScattering'] * u.GeV,
            minPt= 500 * u.MeV,
            impactMax = param_dict['impactMax'] * u.mm,
        ),
        SeedFinderOptionsArg(
             bFieldInZ = 1.99724 * u.T,
        ),
        TrackParamsEstimationConfig(deltaR=(10.0 * u.mm, None)),
        seedingAlgorithm = SeedingAlgorithm.Default,
        geoSelectionConfigFile = oddSeedingSel,
        rnd = rnd,
    )

    # writeTrajectories = False, because those files aren't used for anything, and they
    # are very large.
    acts.examples.reconstruction.addCKFTracks(
        s,
        trackingGeometry,
        field,
        CKFPerformanceConfig(ptMin = 1.0 * u.GeV, nMeasurementsMin = 3),
        writeTrajectories = False,
        outputDirRoot = output_path
    )
    
    s.run()
