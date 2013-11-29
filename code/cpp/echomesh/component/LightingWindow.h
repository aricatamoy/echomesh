#ifndef __ECHOMESH_LIGHTING_WINDOW__
#define __ECHOMESH_LIGHTING_WINDOW__

#include "yaml-cpp/yaml.h"
#include "echomesh/base/Config.h"
#include "echomesh/component/InstrumentGrid.h"

namespace echomesh {

class InstrumentGrid;

class LightingWindow : public DocumentWindow {
 public:
  LightingWindow();

  void setLights(const ColorList& cl) { grid()->setLights(cl); }
  void setConfig(const LightConfig& config);
  void closeButtonPressed();
  InstrumentGrid* grid() { return instrumentGrid_; }

  virtual void moved();

 private:
  InstrumentGrid* instrumentGrid_;
  bool runningInTest_;

  JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(LightingWindow)
};

LightingWindow* makeLightingWindow();

}  // namespace echomesh

#endif  // __ECHOMESH_LIGHTING_WINDOW__
