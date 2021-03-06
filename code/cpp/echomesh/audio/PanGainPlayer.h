#pragma once

#include "echomesh/audio/Envelope.h"
#include "echomesh/audio/EnvelopePlayer.h"

namespace echomesh {
namespace audio {

class PanGainPlayer {
  public:
    PanGainPlayer(Envelope* gain, Envelope* pan);

    void apply(const AudioSourceChannelInfo&);
    void begin();

  private:
    void applyGain(const AudioSourceChannelInfo&);
    void applyPan(const AudioSourceChannelInfo&);

    unique_ptr<EnvelopePlayer> gainPlayer_, panPlayer_;

    DISALLOW_COPY_ASSIGN_AND_LEAKS(PanGainPlayer);
};

}  // namespace audio
}  // namespace echomesh

