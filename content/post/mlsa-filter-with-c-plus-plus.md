---
layout: post
title: "MLSA digital filter のC++実装"
date: 2013-12-01
comments: true
categories: speech-signal-processing speech-synthesis
---

[MLSAフィルタわからん](http://r9y9.github.io/blog/2013/09/23/mlsa-filter-wakaran/)という記事を書いて早2ヶ月、ようやく出来た。

Mel-log spectrum approximate (MLSA) filterというのは、対数振幅スペクトルを近似するようにメルケプストラムから直接音声を合成するデジタルフィルタです。[SPTK](http://sp-tk.sourceforge.net/)のmlsa filterと比較して完全に計算結果が一致したので、間違ってはないはず。MLSAフィルタを使ってメルケプから音声合成するプログラムをC++で自分で書きたいという稀有な人であれば、役に立つと思います。基本的に、SPTKのmlsa filterの再実装です。

# mlsa_filter.h

https://gist.github.com/r9y9/7735120

```cpp
#pragma once

#include <cmath>
#include <memory>
#include <vector>
#include <cassert>

namespace sp {

/**
 * MLSA BASE digital filter (Mel-log Spectrum Approximate digital filter)
 */
class mlsa_base_filter {
public:
  mlsa_base_filter(const int order, const double alpha);

  template <class Vector>
  double filter(const double x, const Vector& b);

 private:
  mlsa_base_filter();

  double alpha_;
  std::vector<double> delay_;
};

mlsa_base_filter::mlsa_base_filter(const int order, const double alpha)
: alpha_(alpha),
  delay_(order+1)
{
}

template <class Vector>
double mlsa_base_filter::filter(const double x, const Vector& b)
{
  double result = 0.0;
  
  delay_[0] = x;
  delay_[1] = (1.0-alpha_*alpha_)*delay_[0] + alpha_*delay_[1];

  for (size_t i = 2; i < b.size(); ++i) {
    delay_[i] = delay_[i] + alpha_*(delay_[i+1]-delay_[i-1]);
    result += delay_[i] * b[i];
  }

  // special case
  // TODO: other solution?
  if (b.size() == 2) {
    result += delay_[1] * b[1];
  } 
  
  // t <- t+1 in time
  for (size_t i = delay_.size()-1; i > 1; --i) {
    delay_[i] = delay_[i-1];
  }
  
  return result;
}

/**
 * MLSA digital filter cascaded
 */
class mlsa_base_cascaded_filter {
 public:
  mlsa_base_cascaded_filter(const int order,
			    const double alpha,
			    const int n_pade);

  template <class Vector>
  double filter(const double x, const Vector& b);
  
 private:
  mlsa_base_cascaded_filter();

  std::vector<std::unique_ptr<mlsa_base_filter>> base_f_; // cascadad filters
  std::vector<double> delay_;
  std::vector<double> pade_coef_;
};

mlsa_base_cascaded_filter::mlsa_base_cascaded_filter(const int order, 
						     const double alpha,
						     const int n_pade)
  : delay_(n_pade + 1),
  pade_coef_(n_pade + 1)
{ 
  using std::unique_ptr;

  if (n_pade != 4 && n_pade != 5) {
    std::cerr << "The number of pade approximations must be 4 or 5."
	      << std::endl;
  }
  assert(n_pade == 4 || n_pade == 5);

  for (int i = 0; i <= n_pade; ++i) {
    mlsa_base_filter* p = new mlsa_base_filter(order, alpha);
    base_f_.push_back(unique_ptr<mlsa_base_filter>(p));
  }
  
  if (n_pade == 4) {
    pade_coef_[0] = 1.0;
    pade_coef_[1] = 4.999273e-1;
    pade_coef_[2] = 1.067005e-1;
    pade_coef_[3] = 1.170221e-2;
    pade_coef_[4] = 5.656279e-4;
  }
  
  if (n_pade == 5) {
    pade_coef_[0] = 1.0;
    pade_coef_[1] = 4.999391e-1;
    pade_coef_[2] = 1.107098e-1;
    pade_coef_[3] = 1.369984e-2;
    pade_coef_[4] = 9.564853e-4;
    pade_coef_[5] = 3.041721e-5;
  }   
}

template <class Vector>
double mlsa_base_cascaded_filter::filter(const double x, const Vector& b)
{
  double result = 0.0;  
  double feed_back = 0.0;

  for (size_t i = pade_coef_.size()-1; i >= 1; --i) {
    delay_[i] = base_f_[i]->filter(delay_[i-1], b);
    double v = delay_[i] * pade_coef_[i];
    if (i % 2 == 1) {
      feed_back += v;
    } else {
      feed_back -= v;
    }
    result += v;
  }

  delay_[0] = feed_back + x;
  result += delay_[0];

  return result;
}

/**
 * MLSA digital filter (Mel-log Spectrum Approximate digital filter)
 * The filter consists of two stage cascade filters
 */
class mlsa_filter {
 public:
  mlsa_filter(const int order, const double alpha, const int n_pade);
 ~mlsa_filter();

 template <class Vector>
 double filter(const double x, const Vector& b);

 private:
 mlsa_filter();

  double alpha_;
  std::unique_ptr<mlsa_base_cascaded_filter> f1_; // first stage
  std::unique_ptr<mlsa_base_cascaded_filter> f2_; // second stage
};

mlsa_filter::mlsa_filter(const int order,
			 const double alpha,
			 const int n_pade)
  : alpha_(alpha),
  f1_(new mlsa_base_cascaded_filter(2, alpha, n_pade)),
  f2_(new mlsa_base_cascaded_filter(order, alpha, n_pade))
{
}

mlsa_filter::~mlsa_filter()
{
}

template <class Vector>
double mlsa_filter::filter(const double x, const Vector& b)
{
  // 1. First stage filtering
  Vector b1 = {0, b[1]};
  double y = f1_->filter(x, b1);
  
  // 2. Second stage filtering
  double result = f2_->filter(y, b);

  return result;
}

} // end namespace sp
```

# 使い方

mlsa_filter.hをインクルードすればおｋ

```
#include "mlsa_filter.h"

// セットアップ
const double alpha = 0.42;
const int order = 30;
const int n_pade = 5;
sp::mlsa_filter mlsa_f(order, alpha, n_pade);

...
// MLSA フィルタリング 
出力一サンプル = mlsa_f.filter(入力一サンプル, フィルタ係数);
```

# 何で再実装したのか

* mlsa filterをC++的なインタフェースで使いたかった
* コード見たらまったく意味がわからなくて、意地でも理解してやろうと思った
* 反省はしている
* 知り合いの声質変換やってる方がMLSAフィルタを波形合成に使ってるっていうし、ちょっとやってみようかなって
* あと最近音声合成の低レベルに手をつけようとと思ってたし勉強にもなるかなって
* 思ったんだ……んだ…だ…

車輪の再開発はあんま良くないと思ってるけど許して。
誰かがリファクタせないかんのだ

# 感想

SPTKのmlsa filterは、正直に言うとこれまで読んできたコードの中で一二を争うほど難解でした（いうてC言語はあまり読んできてないので、Cだとこれが普通なのかもしれないけど）。特に、元コードの d: delayという変数の使われ方が複雑過ぎて、とても読みにくくございました。MLSAフィルタは複数のbase filterのcascade接続で表されるわけだけど、それぞれの遅延が一つのdという変数で管理されていたのです。つまり、

* d[1] ~ d[5] までは、あるフィルタの遅延
* d[6] ~ d[11] までは、別のフィルタの遅延
* d[12] ~ にはまた別のフィルタの遅延

という感じです。

改善しようと思って、base filterというクラスを作ってそのクラスの状態として各フィルタの遅延を持たせて、見通しを良くしました

## さいごに

MLSAフィルタ、難しいですね（小並感

いつかリアルタイム声質変換がやってみたいので、それに使う予定（worldを使うことになるかもしれんけど）。戸田先生当たりがやってる声質変換を一回真似してみたいと思ってる
