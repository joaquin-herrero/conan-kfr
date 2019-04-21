/**
 * KFR (http://kfrlib.com)
 * Copyright (C) 2016  D Levin
 * See LICENSE.txt for details
 */

#include <kfr/base.hpp>
#include <kfr/dsp.hpp>
#include <kfr/io.hpp>

using namespace kfr;

int main()
{
    println(library_version());

    const std::string options = "phaseresp=True";

    univector<fbase, 128> output;
    {
        biquad_params<fbase> bq[] = { biquad_notch(0.1, 0.5), biquad_notch(0.2, 0.5), biquad_notch(0.3, 0.5),
                                      biquad_notch(0.4, 0.5) };
        output                    = biquad(bq, unitimpulse());
    }
    plot_save("biquad_notch", output, options + ", title='Four Biquad Notch filters'");

    {
        biquad_params<fbase> bq[] = { biquad_lowpass(0.2, 0.9) };
        output                    = biquad(bq, unitimpulse());
    }

    println("SVG plots have been saved to svg directory");

    return 0;
}