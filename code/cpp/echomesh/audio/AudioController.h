#ifndef __ECHOMESH_AUDIO_CONTROLLER__
#define __ECHOMESH_AUDIO_CONTROLLER__

#include <map>

#include "echomesh/base/Echomesh.h"

namespace echomesh {

class PlaybackAudioSource;
class SampleAudioSource;

class AudioController {
 public:
  AudioController(Node*);
  virtual ~AudioController();

  void audio();
  PlaybackAudioSource* playbackSource() { return playbackSource_.get(); }

 private:
  typedef uint64 Hash;
  typedef std::map<Hash, SampleAudioSource*> Sources;

  Sources sources_;
  Node* node_;
  ScopedPointer<PlaybackAudioSource> playbackSource_;

  DISALLOW_COPY_AND_ASSIGN(AudioController);
};

}  // namespace echomesh

#endif  // __ECHOMESH_AUDIO_CONTROLLER__
