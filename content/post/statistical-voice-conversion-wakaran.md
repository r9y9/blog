---
layout: post
title: 統計的声質変換クッソムズすぎワロタ（実装の話）
date: 2014-07-13
comments: true
categories: voice-conversion, machine-learning, speech-signal-processing
---

2014/07/28 追記：  
重み行列の構築の部分を改良したのでちょいアップデート。具体的にはdense matrixとして構築してからスパース行列に変換していたのを、はじめからスパース行列として構築するようにして無駄にメモリを使わないようにしました。あとdiffが見やすいようにgistにあげました
https://gist.github.com/r9y9/88bda659c97f46f42525

## まえがき

前回、[統計的声質変換クッソムズすぎワロタ - LESS IS MORE](http://r9y9.github.io/blog/2014/07/05/statistical-voice-conversion-muzui/) という記事を書いたら研究者の方々等ちょいちょい反応してくださって嬉しかったです。差分スペクトル補正、その道の人が聴いても音質がいいそう。これはいい情報です。

Twitter引用:
<blockquote class="twitter-tweet" lang="en"><p>統計的声質変換クッソムズすぎワロタ - LESS IS MORE <a href="http://t.co/8RkeXIf6Ym">http://t.co/8RkeXIf6Ym</a> <a href="https://twitter.com/r9y9">@r9y9</a>さんから ムズすぎと言いながら，最後の音はしっかり出ているあたり凄いなぁ．</p>&mdash; M. Morise (忍者系研究者) (@m_morise) <a href="https://twitter.com/m_morise/statuses/485339123171852289">July 5, 2014</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

<blockquote class="twitter-tweet" lang="en"><p><a href="https://twitter.com/ballforest">@ballforest</a> 従来のパラメータ変換と比較すると、音質は従来よりもよさそうな気はしますがスペクトル包絡の性差ががっつりと影響しそうな気もするんですよね。</p>&mdash; 縄文人（妖精系研究者なのです） (@dicekicker) <a href="https://twitter.com/dicekicker/statuses/485380534122463232">July 5, 2014</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

異性間に関しては、実験が必要ですね。異性間だとF0が結構変わってくると思いますが、差分スペクトル補正の場合そもそもF0をいじらないという前提なので、F0とスペクトル包絡が完全に独立でない（ですよね？）以上、同姓間に比べて音質は劣化する気はします。簡単にやったところ、少なくとも僕の主観的には劣化しました

ところで、結構いい感じにできたぜひゃっはーと思って、先輩に聞かせてみたら違いわかんねと言われて心が折れそうになりました。やはり現実はつらいです。

## 実装の話

さて、今回は少し実装のことを書こうと思います。学習&変換部分はPythonで書いています。その他はGo（※Goの話は書きません）。

## トラジェクトリベースのパラメータ変換が遅いのは僕の実装が悪いからでした本当に申し訳ありませんでしたorz

前回トラジェクトリベースは処理が激重だと書きました。なんと、4秒程度の音声（フレームシフト5msで777フレーム）に対して変換部分に600秒ほどかかっていたのですが（重すぎワロタ）、結果から言えばPythonでも12秒くらいまでに高速化されました（混合数64, メルケプの次元数40+デルタ=80次元、分散共分散はfull）。本当にごめんなさい。

何ヶ月か前、ノリでトラジェクトリベースの変換を実装しようと思ってサクッと書いたのがそのままで、つまりとても効率の悪い実装になっていました。具体的には放置していた問題が二つあって、

- ナイーブな逆行列の計算
- スパース性の無視

です。特に後者はかなりパフォーマンスに影響していました

## ナイーブな逆行列の計算

[numpy.linalg.invとnumpy.linalg.solveを用いた逆行列計算 - 睡眠不足？！ (id:sleepy_yoshi)](http://d.hatena.ne.jp/sleepy_yoshi/20120513/p1)

`numpy.linalg.inv`を使っていましたよね。しかも`numpy.linalg.solve`のほうが速いことを知っていながら。一ヶ月前の自分を問い詰めたい。`numpy.linalg.solve`で置き換えたら少し速くなりました。

- 600秒 -> 570秒 （うろ覚え）

1.05倍の高速化（微妙）

## スパース性の無視

- [T. Toda, A. W. Black, and K. Tokuda, “Voice conversion based on maximum likelihood estimation of spectral parameter trajectory,” IEEE Trans. Audio, Speech, Lang. Process, vol. 15, no. 8, pp. 2222–2235, Nov. 2007](http://isw3.naist.jp/~tomoki/Tomoki/Journals/IEEE-Nov-2007_MLVC.pdf).

論文を見ていただければわかるのですが、トラジェクトリベースの変換法における多くの計算は、行列を使って表すことができます。で、論文中の$W$という行列は、サイズがめちゃくちゃでかいのですがほとんどの要素は0です。この性質を使わない理由はないですよね？？

…残念なことに、僕は密行列として扱って計算していました。ほら、疎行列ってちょっと扱いづらいじゃないですか…めんどくさそう…と思って放置してました。ごめんなさい

pythonで疎行列を扱うなら、scipy.sparseを使えば良さそうです。結果、$W$を疎行列として扱うことで行列演算は大きく高速化されました。

- 570秒 -> 12秒くらい

単純に考えると50倍の高速化ですか。本当にアホだった。最初からscipy.sparse使っておけばよかったです。

scipy.sparseの使い方は以下を参考にしました。みなさんぜひ使いましょう

- [Python で疎行列(SciPy) - 唯物是真 @Scaled_Wurm](http://sucrose.hatenablog.com/entry/2013/04/07/130625)
- [Sparse matrices (scipy.sparse) — SciPy v0.14.0 Reference Guide](http://docs.scipy.org/doc/scipy/reference/sparse.html)
- [scipy.sparseで疎行列の行列積 | frontier45](http://lucidfrontier45.wordpress.com/2011/08/02/scipysparse_matmul/)

## コード

メモ的な意味で主要なコードを貼っておきます。
https://gist.github.com/r9y9/88bda659c97f46f42525

```python
#!/usr/bin/python
# coding: utf-8

import numpy as np
from numpy import linalg
from sklearn.mixture import GMM
import scipy.linalg
import scipy.sparse
import scipy.sparse.linalg

class GMMMap:
    """GMM-based frame-by-frame speech parameter mapping. 

    GMMMap represents a class to transform spectral features of a source
    speaker to that of a target speaker based on Gaussian Mixture Models
    of source and target joint spectral features.
    
    Notation
    --------
    Source speaker's feature: X = {x_t}, 0 <= t < T
    Target speaker's feature: Y = {y_t}, 0 <= t < T
    where T is the number of time frames.

    Parameters
    ----------
    gmm : scipy.mixture.GMM
        Gaussian Mixture Models of source and target joint features
    
    swap : bool
        True: source -> target
        False target -> source
    
    Attributes
    ----------
    num_mixtures : int
        the number of Gaussian mixtures

    weights : array, shape (`num_mixtures`)
        weights for each gaussian

    src_means : array, shape (`num_mixtures`, `order of spectral feature`)
        means of GMM for a source speaker

    tgt_means : array, shape (`num_mixtures`, `order of spectral feature`)
        means of GMM for a target speaker

    covarXX : array, shape (`num_mixtures`, `order of spectral feature`, 
        `order of spectral feature`)
        variance matrix of source speaker's spectral feature

    covarXY : array, shape (`num_mixtures`, `order of spectral feature`, 
        `order of spectral feature`)
        covariance matrix of source and target speaker's spectral feature

    covarYX : array, shape (`num_mixtures`, `order of spectral feature`, 
        `order of spectral feature`)
        covariance matrix of target and source speaker's spectral feature

    covarYY : array, shape (`num_mixtures`, `order of spectral feature`, 
        `order of spectral feature`)
        variance matrix of target speaker's spectral feature
    
    D : array, shape (`num_mixtures`, `order of spectral feature`, 
        `order of spectral feature`)
        covariance matrices of target static spectral features

    px : scipy.mixture.GMM
        Gaussian Mixture Models of source speaker's features

    Reference
    ---------
      - [Toda 2007] Voice Conversion Based on Maximum Likelihood Estimation
        of Spectral Parameter Trajectory.
        http://isw3.naist.jp/~tomoki/Tomoki/Journals/IEEE-Nov-2007_MLVC.pdf

    """
    def __init__(self, gmm, swap=False):
        # D is the order of spectral feature for a speaker
        self.num_mixtures, D = gmm.means_.shape[0], gmm.means_.shape[1]/2
        self.weights = gmm.weights_

        # Split source and target parameters from joint GMM
        self.src_means = gmm.means_[:, 0:D]
        self.tgt_means = gmm.means_[:, D:]
        self.covarXX = gmm.covars_[:, :D, :D]
        self.covarXY = gmm.covars_[:, :D, D:]
        self.covarYX = gmm.covars_[:, D:, :D]
        self.covarYY = gmm.covars_[:, D:, D:]

        # swap src and target parameters
        if swap:
            self.tgt_means, self.src_means = self.src_means, self.tgt_means
            self.covarYY, self.covarXX = self.covarXX, self.covarYY
            self.covarYX, self.covarXY = self.XY, self.covarYX

        # Compute D eq.(12) in [Toda 2007]
        self.D = np.zeros(self.num_mixtures*D*D).reshape(self.num_mixtures, D, D)
        for m in range(self.num_mixtures):
            xx_inv_xy = np.linalg.solve(self.covarXX[m], self.covarXY[m])
            self.D[m] = self.covarYY[m] - np.dot(self.covarYX[m], xx_inv_xy)

        # p(x), which is used to compute posterior prob. for a given source
        # spectral feature in mapping stage.
        self.px = GMM(n_components=self.num_mixtures, covariance_type="full")
        self.px.means_ = self.src_means
        self.px.covars_ = self.covarXX
        self.px.weights_ = self.weights

    def convert(self, src):
        """
        Mapping source spectral feature x to target spectral feature y 
        so that minimize the mean least squared error.
        More specifically, it returns the value E(p(y|x)].

        Parameters
        ----------
        src : array, shape (`order of spectral feature`)
            source speaker's spectral feature that will be transformed

        Return
        ------
        converted spectral feature
        """
        D = len(src)

        # Eq.(11)
        E = np.zeros((self.num_mixtures, D))
        for m in range(self.num_mixtures):
            xx = np.linalg.solve(self.covarXX[m], src - self.src_means[m])
            E[m] = self.tgt_means[m] + self.covarYX[m].dot(xx)
                
        # Eq.(9) p(m|x)
        posterior = self.px.predict_proba(np.atleast_2d(src))

        # Eq.(13) conditinal mean E[p(y|x)]
        return posterior.dot(E)
            
class TrajectoryGMMMap(GMMMap):
    """
    Trajectory-based speech parameter mapping for voice conversion
    based on the maximum likelihood criterion.

    Parameters
    ----------
    gmm : scipy.mixture.GMM
        Gaussian Mixture Models of source and target speaker joint features

    gv : scipy.mixture.GMM (default=None)
        Gaussian Mixture Models of target speaker's global variance of spectral
        feature
    
    swap : bool (default=False)
        True: source -> target
        False target -> source

    Attributes
    ----------
    TODO 

    Reference
    ---------
      - [Toda 2007] Voice Conversion Based on Maximum Likelihood Estimation
        of Spectral Parameter Trajectory.
        http://isw3.naist.jp/~tomoki/Tomoki/Journals/IEEE-Nov-2007_MLVC.pdf
    """
    def __init__(self, gmm, T, gv=None, swap=False):
        GMMMap.__init__(self, gmm, swap)

        self.T = T
        # shape[1] = d(src) + d(src_delta) + d(tgt) + d(tgt_delta)
        D = gmm.means_.shape[1] / 4

        ## Setup for Trajectory-based mapping
        self.__construct_weight_matrix(T, D)

        ## Setup for GV post-filtering
        # It is assumed that GV is modeled as a single mixture GMM
        if gv != None:
            self.gv_mean = gv.means_[0]
            self.gv_covar = gv.covars_[0]
            self.Pv = np.linalg.inv(self.gv_covar)

    def __construct_weight_matrix(self, T, D):
        # Construct Weight matrix W
        # Eq.(25) ~ (28)
        for t in range(T):
            w0 = scipy.sparse.lil_matrix((D, D*T))
            w1 = scipy.sparse.lil_matrix((D, D*T))
            w0[0:,t*D:(t+1)*D] = scipy.sparse.diags(np.ones(D), 0)

            if t-1 >= 0:
                tmp = np.zeros(D)
                tmp.fill(-0.5)
                w1[0:,(t-1)*D:t*D] = scipy.sparse.diags(tmp, 0)
            if t+1 < T:
                tmp = np.zeros(D)
                tmp.fill(0.5)
                w1[0:,(t+1)*D:(t+2)*D] = scipy.sparse.diags(tmp, 0)

            W_t = scipy.sparse.vstack([w0, w1])

            # Slower
            # self.W[2*D*t:2*D*(t+1),:] = W_t

            if t == 0:
                self.W = W_t
            else:
                self.W = scipy.sparse.vstack([self.W, W_t])

        self.W = scipy.sparse.csr_matrix(self.W)

        assert self.W.shape == (2*D*T, D*T)
        
    def convert(self, src):
        """
        Mapping source spectral feature x to target spectral feature y 
        so that maximize the likelihood of y given x.

        Parameters
        ----------
        src : array, shape (`the number of frames`, `the order of spectral feature`)
            a sequence of source speaker's spectral feature that will be
            transformed

        Return
        ------
        a sequence of transformed spectral features
        """
        T, D = src.shape[0], src.shape[1]/2

        if T != self.T:
            self.__construct_weight_matrix(T, D)

        # A suboptimum mixture sequence  (eq.37)
        optimum_mix = self.px.predict(src)

        # Compute E eq.(40)
        self.E = np.zeros((T, 2*D))
        for t in range(T):
            m = optimum_mix[t] # estimated mixture index at time t
            xx = np.linalg.solve(self.covarXX[m], src[t] - self.src_means[m])
            # Eq. (22)
            self.E[t] = self.tgt_means[m] + np.dot(self.covarYX[m], xx)
        self.E = self.E.flatten()

        # Compute D eq.(41). Note that self.D represents D^-1.
        self.D = np.zeros((T, 2*D, 2*D))
        for t in range(T):
            m = optimum_mix[t]
            xx_inv_xy = np.linalg.solve(self.covarXX[m], self.covarXY[m])
            # Eq. (23)
            self.D[t] = self.covarYY[m] - np.dot(self.covarYX[m], xx_inv_xy)
            self.D[t] = np.linalg.inv(self.D[t])
        self.D = scipy.linalg.block_diag(*self.D)

        # represent D as a sparse matrix
        self.D = scipy.sparse.csr_matrix(self.D)

        # Compute target static features
        # eq.(39)
        covar = self.W.T.dot(self.D.dot(self.W))
        y = scipy.sparse.linalg.spsolve(covar, self.W.T.dot(self.D.dot(self.E)),\
                                        use_umfpack=False)
        return y.reshape((T, D))
```

## 結論

- 疎行列の演算を考えるときは、間違ってもめんどくさいとか思わずに疎行列を積極的に使おう
- 統計的声質変換ムズすぎ

## おまけめも

僕が変換精度を改善するために考えていることのめも

- 統計的な手法を使う限りover-smoothingの問題はついてくる。ならば、逆にover-smoothingされることで都合の良い特徴量を考えることはできないか
- メルケプとかそもそもスペクトル包絡をコンパクトにparamtricに表現するために考えられたもの（だと思ってる）ので、高品質な変換を考えるならばスペクトル包絡をそのまま使うなりした方がいいんじゃないか。とはいえスペクトル包絡をそのまま使うのはぼちぼち高次元なので、個人性に依存する部分を残した形で非線形次元削減したらどうか（例えばニューラルネットを使って統計的に個人性に依存する部分を見つけ出すとか）
- time-dependentな関係をモデル化しないとだめじゃないか、確率モデルとして。RNNとか普通に使えそうだし、まぁHMMでもよい
- 音素境界を推定して、segment単位で変換するのも良いかも
- 識別モデルもっと使ってもいいんじゃないか
- 波形合成にSPTKのmlsadfコマンド使ってる？あれ実はフレーム間のメルケプが線形補間されてるんですよね。本当に線形補間でいいんでしょうか？他の補間法も試したらどうですかね

こんなかんじですか。おやすみなさい
