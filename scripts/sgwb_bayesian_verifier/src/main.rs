use serde::{Deserialize, Serialize};
use std::fs::File;
use std::io::BufReader;

#[derive(Serialize, Deserialize, Debug)]
struct InputData {
    frequencies_hz: Vec<f64>,
    data_strain: Vec<f64>,
    data_errors: Vec<f64>,
}

#[derive(Serialize, Deserialize, Debug)]
struct OutputData {
    bic_h0: f64,
    bic_h1: f64,
    delta_bic: f64,
    ln_bayes_factor: f64,
    bayes_factor: f64,
    verdict: String,
}

const F_YEAR: f64 = 1.0 / (365.25 * 86400.0);
const F_COMPTON: f64 = 2.418e-8;

fn model_h0(freqs: &[f64], log10_a: f64, gamma: f64) -> Vec<f64> {
    let a = 10_f64.powf(log10_a);
    let slope_exp = (3.0 - gamma) / 2.0;
    freqs.iter().map(|&f| a * (f / F_YEAR).powf(slope_exp)).collect()
}

fn model_h1(freqs: &[f64], log10_a_oligon: f64, gamma_oligon: f64, log10_a_res: f64) -> Vec<f64> {
    let a_oligon = 10_f64.powf(log10_a_oligon);
    let slope_exp = (3.0 - gamma_oligon) / 2.0;
    let a_res = 10_f64.powf(log10_a_res);
    let sigma_f = 0.15 * F_COMPTON;

    freqs.iter().map(|&f| {
        let continuum = a_oligon * (f / F_YEAR).powf(slope_exp);
        let resonance = a_res * (-0.5 * ((f - F_COMPTON) / sigma_f).powi(2)).exp();
        continuum + resonance
    }).collect()
}

fn log_likelihood(data_strain: &[f64], data_errors: &[f64], model_strain: &[f64]) -> f64 {
    let mut ll = 0.0;
    for i in 0..data_strain.len() {
        let res = (data_strain[i] - model_strain[i]) / (data_errors[i] + 1e-25);
        let chi2 = res.powi(2);
        let log_norm = (2.0 * std::f64::consts::PI * (data_errors[i].powi(2) + 1e-50)).ln();
        ll += -0.5 * (chi2 + log_norm);
    }
    ll
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let file = File::open("input.json")?;
    let reader = BufReader::new(file);
    let input: InputData = serde_json::from_reader(reader)?;

    let freqs = &input.frequencies_hz;
    let data_strain = &input.data_strain;
    let data_errors = &input.data_errors;
    let n = freqs.len() as f64;

    // H0
    let mut best_ll_h0 = -1e9;
    for a in -160..-130 {
        let log10_a = a as f64 / 10.0;
        let m = model_h0(freqs, log10_a, 4.33);
        let ll = log_likelihood(data_strain, data_errors, &m);
        if ll > best_ll_h0 { best_ll_h0 = ll; }
    }

    // H1
    let mut best_ll_h1 = -1e9;
    for a_ol in -160..-135 {
        let log10_a_oligon = a_ol as f64 / 10.0;
        for g_ol in [35, 38, 40, 43] {
            let gamma_oligon = g_ol as f64 / 10.0;
            for a_r in -160..-140 {
                let log10_a_res = a_r as f64 / 10.0;
                let m = model_h1(freqs, log10_a_oligon, gamma_oligon, log10_a_res);
                let ll = log_likelihood(data_strain, data_errors, &m);
                if ll > best_ll_h1 { best_ll_h1 = ll; }
            }
        }
    }

    let k_h0 = 1.0;
    let k_h1 = 3.0;
    let bic_h0 = k_h0 * n.ln() - 2.0 * best_ll_h0;
    let bic_h1 = k_h1 * n.ln() - 2.0 * best_ll_h1;
    let delta_bic = bic_h0 - bic_h1;
    let ln_bayes_factor = 0.5 * delta_bic;
    
    let verdict = if ln_bayes_factor > 5.0 {
        "DECISIVE_EVIDENCE_FOR_K4_OLIGON_PREGEOMETRY"
    } else if ln_bayes_factor > 2.5 {
        "STRONG_EVIDENCE_FOR_K4_OLIGON_PREGEOMETRY"
    } else if ln_bayes_factor > 1.0 {
        "MODERATE_EVIDENCE"
    } else {
        "INCONCLUSIVE_OR_SMBHB_FAVORED"
    };

    let output = OutputData {
        bic_h0,
        bic_h1,
        delta_bic,
        ln_bayes_factor,
        bayes_factor: ln_bayes_factor.min(700.0).exp(),
        verdict: verdict.to_string(),
    };

    let out_file = File::create("output.json")?;
    serde_json::to_writer_pretty(out_file, &output)?;

    Ok(())
}
