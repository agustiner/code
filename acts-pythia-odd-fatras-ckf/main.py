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
from acts.examples.odd import getOpenDataDetector
import datetime
import os

def getActsSourcePath():
    return pathlib.Path("/home/user1/code/acts/source")

def getOpenDataDetectorPath():
    return getActsSourcePath() / "thirdparty" / "OpenDataDetector"


logger = acts.logging.getLogger("full_chain_odd")
logger.info("Starting full_chain_odd")
u = acts.UnitConstants
oddPath = getOpenDataDetectorPath()
outputDir = pathlib.Path.cwd() / datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
os.mkdir(outputDir)
os.mkdir(outputDir / 'pythia')
os.mkdir(outputDir / 'fatras')
os.mkdir(outputDir / 'digitization')
os.mkdir(outputDir / 'seeding')
os.mkdir(outputDir / 'ckf')
os.mkdir(outputDir / 'vertexfitting')

# acts.examples.dump_args_calls(locals())  # show python binding calls
oddMaterialMap = oddPath / "data/odd-material-maps.root"
oddDigiConfig = oddPath / "config/odd-digi-smearing-config.json"
oddSeedingSel = oddPath / "config/odd-seeding-config.json"
oddMaterialDeco = acts.IMaterialDecorator.fromFile(oddMaterialMap)

detector, trackingGeometry, decorators = getOpenDataDetector(
    oddPath, mdecorator=oddMaterialDeco
)
field = acts.ConstantBField(acts.Vector3(0.0, 0.0, 2.0 * u.T))
rnd = acts.examples.RandomNumbers(seed=42)

s = acts.examples.Sequencer(events=1, numThreads=-1, outputDir=str(outputDir))

logger.info('Using pythia to make ttbar events.')

acts.examples.simulation.addPythia8(
    s,
    hardProcess=["Top:qqbar2ttbar=on"],
    npileup=10,
    vtxGen=acts.examples.GaussianVertexGenerator(
        stddev=acts.Vector4(0.0125 * u.mm, 0.0125 * u.mm, 55.5 * u.mm, 5.0 * u.ns),
        mean=acts.Vector4(0, 0, 0, 0),
    ),
    rnd=rnd,
    outputDirRoot=outputDir / 'pythia',
)

acts.examples.simulation.addFatras(
    s,
    trackingGeometry,
    field,
    ParticleSelectorConfig(eta=(-3.0, 3.0), pt=(150 * u.MeV, None), removeNeutral=True),
    outputDirRoot=outputDir / 'fatras',
    rnd=rnd,
)

acts.examples.simulation.addDigitization(
    s,
    trackingGeometry,
    field,
    digiConfigFile=oddDigiConfig,
    outputDirRoot=outputDir / 'digitization',
    rnd=rnd,
)

acts.examples.reconstruction.addSeeding(
    s,
    trackingGeometry,
    field,
    TruthSeedRanges(pt=(1.0 * u.GeV, None), eta=(-3.0, 3.0), nHits=(9, None)),
    geoSelectionConfigFile=oddSeedingSel,
    outputDirRoot=outputDir / 'seeding',
)

acts.examples.reconstruction.addCKFTracks(
    s,
    trackingGeometry,
    field,
    CKFPerformanceConfig(ptMin=1.0 * u.GeV, nMeasurementsMin=6),
    outputDirRoot=outputDir / 'ckf',
)

acts.examples.reconstruction.addVertexFitting(
    s,
    field,
    TrackSelectorRanges(pt=(1.0 * u.GeV, None), absEta=(None, 3.0), removeNeutral=True),
    vertexFinder=VertexFinder.Iterative,
    trajectories="trajectories",
    outputDirRoot=outputDir / 'vertexfitting'
)

s.run()
