#ifndef __ECHOMESH_INSTRUMENT_COMPONENT__
#define __ECHOMESH_INSTRUMENT_COMPONENT__

#include "echomesh/base/Echomesh.h"
#include "echomesh/base/Config.h"

namespace echomesh {

class InstrumentComponent : public Component {
 public:
  InstrumentComponent();
  ~InstrumentComponent() {}

  void configure(const String& label, const Instrument&);

  void setColor(const Colour&);
  virtual void paint(Graphics&);
  void setShape(bool isRect);
  void setLabelPadding(int x, int y);
  void setShowLabel(bool show);
  void setLabel(const String&);

 private:
  String label_;
  Colour color_;
  Colour labelColor_;
  CriticalSection lock_;

  bool isRect_;
  int labelPaddingX_;
  int labelPaddingY_;
  bool showLabel_;

  JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(InstrumentComponent)
};

}  // namespace echomesh

#endif  // __ECHOMESH_INSTRUMENT_COMPONENT__
