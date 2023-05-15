//VERSION=3

function setup() {
  return {
    input: [{
        bands: ["MLT72"]
    }],
    output: {
        bands: 1,
        sampleType: SampleType.FLOAT32,
        nodataValue: -9999
    },
    mosaicking: Mosaicking.TILE
  }
}

function evaluatePixel(samples) {
    for (let i = 0; i < samples.length; i++){
        var tile = samples[i]
        if (tile.MLT72 > 0){
            return [tile.MLT72]
        }
    }
    return [0]
}
