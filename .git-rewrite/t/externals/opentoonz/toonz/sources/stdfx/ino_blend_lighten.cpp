//------------------------------------------------------------
#include "tfxparam.h"
#include "stdfx.h"

#include "ino_common.h"
#include "igs_color_blend.h"
/* tnzbase --> Source Files --> tfx --> binaryFx.cppを参照 */
class ino_blend_lighten final : public TBlendForeBackRasterFx {
  FX_PLUGIN_DECLARATION(ino_blend_lighten)

public:
  ino_blend_lighten() : TBlendForeBackRasterFx(false) {}
  ~ino_blend_lighten() {}
  void brendKernel(double& dnr, double& dng, double& dnb, double& dna,
                   const double upr, double upg, double upb, double upa,
                   const double up_opacity,
                   const bool alpha_rendering_sw = true,
                   const bool is_xyz             = false) override {
    igs::color::lighten(dnr, dng, dnb, dna, upr, upg, upb, upa, up_opacity,
                        !is_xyz);
  }
};
FX_PLUGIN_IDENTIFIER(ino_blend_lighten, "inoLightenFx");
