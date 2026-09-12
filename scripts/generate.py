"""Generate presentation data and scientific figures from the included inputs."""
from pathlib import Path
import csv
import json
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
ASSETS = ROOT / 'site/assets'
ASSETS.mkdir(parents=True, exist_ok=True)
INK, MUTED, PAPER, BLUE, RUST, GREEN = '#252e30', '#667070', '#f5f3ec', '#427e9c', '#b95238', '#367869'
CMAP = LinearSegmentedColormap.from_list('recovery', ['#e9ebe4', '#abc5b6', '#438d7a', '#154c43'])
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10, 'text.color': INK,
                     'axes.labelcolor': INK, 'xtick.color': MUTED, 'ytick.color': MUTED,
                     'axes.edgecolor': '#c9d0c8', 'figure.facecolor': PAPER, 'axes.facecolor': PAPER,
                     'savefig.facecolor': PAPER, 'axes.spines.top': False, 'axes.spines.right': False,
                     'svg.fonttype': 'path'})

def read_csv(name):
    with (DATA / name).open(newline='', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))

def save(fig, name):
    fig.savefig(ASSETS / f'{name}.svg', bbox_inches='tight')
    fig.savefig(ASSETS / f'{name}.png', dpi=150, bbox_inches='tight')
    plt.close(fig)

def analytic(t, km=1.04, dm=.35, kp=7.70, dp=.02):
    """Zero initial state; constant input; dimensional M1 cascade."""
    m = km / dm * (1 - np.exp(-dm * t))
    p = km * kp / dm * ((1-np.exp(-dp*t))/dp - (np.exp(-dm*t)-np.exp(-dp*t))/(dp-dm))
    return np.column_stack([m, p])

def model_data():
    t = np.linspace(0, 160, 161)
    y = analytic(t)
    ref = solve_ivp(lambda _, v: (1.04-.35*v[0], 7.70*v[0]-.02*v[1]),
                    (0, 160), (0, 0), t_eval=t, method='DOP853', rtol=1e-11, atol=1e-12)
    error = np.max(np.abs(ref.y.T-y))/np.max(y)
    assert error < 1e-9
    for c in (.25, .5, 2, 4):
        shifted = analytic(t, km=1.04*c, kp=7.7/c)
        assert np.allclose(shifted[:,1], y[:,1], rtol=1e-12, atol=1e-10)
        assert np.allclose(shifted[:,0], c*y[:,0])
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.7))
    for ax, col, label in zip(axes, [1, 0], ['Protein', 'mRNA']):
        normal = y[:,col]/y[:,col].max()
        ax.plot(t, normal, color=BLUE, lw=2.5, label='Reference rates')
        ax.plot(t, normal*(2 if col==0 else 1), color=RUST, lw=2, ls='--', label='2× transcription, ½× translation')
        ax.set(xlabel='Time (minutes)', ylabel='Relative to reference peak', title=label)
        ax.grid(alpha=.18)
    axes[0].legend(loc='lower right', fontsize=8)
    fig.tight_layout(w_pad=3)
    save(fig, 'rate-ambiguity')
    # A two-rate fit-error map, with degradation rates held fixed. This is not a posterior.
    scale = np.geomspace(.25, 4, 81)
    xx, yy = np.meshgrid(scale, scale)
    protein_error = (xx*yy-1)**2 * np.mean((y[:,1]/y[:,1].max())**2)
    both_error = .5*(protein_error + (xx-1)**2*np.mean((y[:,0]/y[:,0].max())**2))
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.0))
    for ax, values, title in zip(axes, [protein_error, both_error], ['Protein only', 'Protein + mRNA']):
        z = np.log10(values + 1e-6)
        ax.contourf(np.log2(scale), np.log2(scale), z, levels=np.linspace(-6, 2, 25), cmap='Blues_r', extend='both')
        ax.contour(np.log2(scale), np.log2(scale), values, levels=[.001, .01, .1], colors='#789dad', linewidths=.7)
        ax.scatter([0], [0], c='#f8ce8a', s=36, edgecolor=INK, linewidth=.6)
        ax.set(title=title, xlabel='Transcription rate / reference', ylabel='Translation rate / reference',
               xticks=[-2,-1,0,1,2], yticks=[-2,-1,0,1,2], xticklabels=['¼','½','1','2','4'], yticklabels=['¼','½','1','2','4'])
    fig.text(.5, -.01, 'Darker = smaller fit error. Simulated noiseless traces; degradation rates held fixed.', ha='center', fontsize=9, color=MUTED)
    fig.tight_layout(w_pad=2.5)
    save(fig, 'fit-landscape')
    return {'t': t.tolist(), 'mrna': y[:,0].tolist(), 'protein': y[:,1].tolist(),
            'rates': {'km':1.04,'dm':.35,'kp':7.7,'dp':.02}, 'closedFormOdeError': float(error)}

def network_data():
    rows = [{k:(v if k=='method' else float(v)) for k,v in r.items()} for r in read_csv('network-grid.csv')]
    assert all(r['n_genes']==100 and r['n_seeds']==5 and r['entanglement']==0 for r in rows)
    for r in rows:
        expected=(r['aupr']-r['true_edge_density'])/(1-r['true_edge_density'])
        assert abs(r['normalized_recovery']-expected)<1e-12
    rhos = sorted({r['rho'] for r in rows})
    snrs = sorted({r['snr'] for r in rows}, reverse=True)
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.8), sharey=True)
    for ax, method, title in zip(axes, ['raw','deflate1'], ['Raw responses', 'Remove the largest shared component']):
        z=np.array([[next(r['normalized_recovery'] for r in rows if r['method']==method and r['rho']==rho and r['snr']==snr) for rho in rhos] for snr in snrs])
        im=ax.imshow(z,cmap=CMAP,vmin=0,vmax=.75,aspect='auto')
        ax.set(title=title, xticks=range(len(rhos)), xticklabels=[f'{x:g}' for x in rhos],
               yticks=range(len(snrs)), yticklabels=[f'{x:g}' for x in snrs], xlabel='Shared-component mixing weight ρ')
        for i in range(z.shape[0]):
            for j in range(z.shape[1]):
                ax.text(j,i,f'{z[i,j]:.2f}', ha='center', va='center', fontsize=8, color='white' if z[i,j]>.40 else INK)
    axes[0].set_ylabel('Specific signal / noise')
    fig.subplots_adjust(bottom=.19, top=.87, right=.9, wspace=.12)
    cax=fig.add_axes([.92,.23,.016,.56])
    fig.colorbar(im,cax=cax,label='Normalized average precision')
    fig.text(.08,.04,'100 genes · 5 seeds per cell · Simulated rank-1 shared component',fontsize=9,color=MUTED)
    save(fig, 'network-recovery')
    return {'rows': rows, 'rhos':rhos, 'snrs':snrs}

METHODS={'lagged_genie3_rf':'Lagged random forest', 'lagged_lasso':'Lagged LASSO', 'lagged_correlation':'Lagged correlation', 'dmd_operator':'Dynamical operator', 'static_correlation':'Static correlation'}
def benchmark_data():
    result={}
    for dataset in ['dream4','boolode']:
        raw=read_csv(f'benchmark-{dataset}.csv')
        result[dataset]={'count':len(raw), 'methods':[{'id':k,'label':v,'mean':float(np.mean([float(r[k]) for r in raw])), 'values':[float(r[k]) for r in raw]} for k,v in METHODS.items()]}
    fig, axes=plt.subplots(1,2,figsize=(10.5,4.2),sharex=True)
    for ax, dataset, title in zip(axes,['dream4','boolode'],['DREAM4 · 5 networks','BoolODE · 18 datasets']):
        m=sorted(result[dataset]['methods'],key=lambda x:x['mean'],reverse=True)
        for i,r in enumerate(m):
            color=RUST if r['id']=='dmd_operator' else GREEN
            ax.barh(i,r['mean'],color=color,height=.48,alpha=.85)
            ax.text(r['mean']+.008,i,f"{r['mean']:.3f}",va='center',fontsize=9)
        ax.set(yticks=range(5),yticklabels=[x['label'] for x in m],xlim=(0,.66),xlabel='Mean average precision',title=title)
        ax.invert_yaxis()
    fig.tight_layout(w_pad=3)
    save(fig,'network-benchmarks')
    return result

def brightness_data():
    result=[]
    keys=['ratio_input','ratio_target','ratio_prediction','ratio_unchanged','ratio_target_reconstruction']
    for seed in range(3):
        d=json.loads((DATA/f'brightness-seed-{seed}.json').read_text())
        assert set(d['test_base_ids']).isdisjoint(d['training_direction_base_ids'])
        a=np.load(DATA/f'brightness-seed-{seed}.npz')
        assert np.allclose(a['ratio_target'],1.5*a['ratio_input'],atol=1e-7)
        samples=[]
        for i in range(3):
            paths={}
            for key in keys:
                filename=f'brightness-{seed}-{i}-{key}.png'
                im=Image.fromarray(np.round(np.clip(a[key][i],0,1)*255).astype(np.uint8))
                im.save(ASSETS/filename)
                paths[key]=filename
            samples.append({'base':d['test_base_ids'][i], 'images':paths,
                            'exampleMse':float(np.mean((a['ratio_prediction'][i]-a['ratio_target'][i])**2))})
        result.append({'seed':seed,'gain':d['ratio_gain'],'editedMse':d['ratio_decoded_mse'],
                       'unchangedMse':d['ratio_unedited_mse'], 'targetReconstructionMse':d['ratio_target_reconstruction_mse'],
                       'improvement':1-d['ratio_decoded_mse']/d['ratio_unedited_mse'],
                       'shiftResidual':d['ratio_latent_shift_residual'], 'affineResidual':d['ratio_latent_affine_residual'], 'samples':samples})
    fig,axes=plt.subplots(3,3,figsize=(7.5,7.0))
    a=np.load(DATA/'brightness-seed-0.npz')
    for i in range(3):
        for j,key in enumerate(keys[:3]):
            axes[i,j].imshow(np.clip(a[key][i],0,1),interpolation='nearest')
            axes[i,j].set(xticks=[],yticks=[])
            if i==0: axes[i,j].set_title(['Input','Target: 1.5× brighter','Decoded edit'][j],fontsize=10,pad=12)
            for s in axes[i,j].spines.values():s.set_visible(False)
    fig.text(.5,.02,'All three held-out examples, seed 0 · 32 × 32 pixels · Display clipped to [0, 1]',ha='center',fontsize=9,color=MUTED)
    fig.tight_layout(rect=[0,.04,1,1],h_pad=.8,w_pad=.8)
    save(fig,'brightness-examples')
    return result

def classification_data():
    raw=json.loads((DATA/'classification.json').read_text())
    labels={'nearest mean':'Nearest mean', 'remove subspace':'Remove 8 directions',
            'validation-weighted subspace':'Weight 8 directions','regularized LDA':'Regularized LDA',
            'logistic regression':'Logistic regression','nearest neighbors':'Nearest neighbors',
            'paired-blur augmentation':'Paired blur + logistic'}
    fig,axes=plt.subplots(1,2,figsize=(11,5.0),sharey=True)
    for ax,regime,title in zip(axes,['independent','correlated'],['Training blur independent of class','Training blur correlated with class']):
        records=[r for r in raw['summary'] if r['regime']==regime]
        for i,r in enumerate(records):
            values=[float(v['accuracy'][r['method']]) for v in raw['records'] if v['regime']==regime]
            assert abs(np.mean(values)-r['mean_accuracy'])<1e-12
            color=RUST if r['method']=='paired-blur augmentation' else GREEN
            ax.errorbar(r['mean_accuracy'],i,xerr=r['split_sd'],fmt='o',color=color,capsize=3)
            ax.text(1.005,i,f"{100*r['mean_accuracy']:.1f}%",fontsize=9,va='center')
        ax.set(yticks=range(len(records)),yticklabels=[labels[r['method']] for r in records],
               xlim=(.66,1.065),xticks=[.7,.8,.9,1],xticklabels=['70%','80%','90%','100%'],title=title,xlabel='Held-out image accuracy')
        ax.grid(axis='x',alpha=.25)
    axes[0].invert_yaxis()
    fig.text(.5,.02,'10 splits · Error bars: split SD · Paired augmentation receives extra renderings',ha='center',fontsize=9,color=MUTED)
    fig.tight_layout(rect=[0,.05,1,1],w_pad=2)
    save(fig,'classification')
    return raw['summary']

def input_design_data():
    d=json.loads((DATA/'input-design.json').read_text())
    rows=[r for r in d['summary'] if r['kappa']==.02]
    assert sorted((r['truth'],r['protocol'],r['correct'],r['n']) for r in rows)==[
        ('M2','constant',83,100),('M2','three_pulses',100,100),
        ('M3','constant',61,100),('M3','three_pulses',99,100)]
    fig,ax=plt.subplots(figsize=(10,4.6))
    for i,model in enumerate(['M2','M3']):
        for j,protocol in enumerate(['constant','three_pulses']):
            row=next(r for r in rows if r['truth']==model and r['protocol']==protocol)
            n=row['n']; p=row['correct']/n; z=1.96
            center=(p+z*z/(2*n))/(1+z*z/n)
            half=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/(1+z*z/n)
            y=i+(-.17 if j==0 else .17)
            color=BLUE if j==0 else GREEN
            ax.barh(y,p*100,height=.25,color=color,label=['Constant input','Three pulses'][j] if i==0 else None)
            ax.errorbar(p*100,y,xerr=[[max(0,p-center+half)*100],[max(0,center+half-p)*100]],color=INK,capsize=3,lw=1)
            ax.text(104,y,f"{row['correct']} / {n}",va='center',fontsize=12)
    ax.set(yticks=[0,1],yticklabels=['Feedback slows\nmRNA production','Feedback slows\nprotein production'],
           xlim=(0,121),xticks=[0,25,50,75,100],xlabel='Correct model selections (%)')
    ax.invert_yaxis();ax.legend(loc='upper center',bbox_to_anchor=(.5,1.18),ncol=2,frameon=False)
    fig.text(.5,.01,'Same total input · 80 observations · 300 minutes · 100 noisy trials per condition',ha='center',fontsize=10,color=MUTED)
    fig.tight_layout(rect=[0,.06,1,.99]);save(fig,'input-design')
    return d

def transfer_data():
    rows=read_csv('brightness-transfer.csv')
    assert len(rows)==360 and all(int(r['n_bases'])==96 for r in rows)
    fig,ax=plt.subplots(figsize=(10,4.5))
    ratios=sorted({float(r['ratio']) for r in rows})
    groups=[('trained','affine_group','Fitted scaling rule',GREEN),
            ('trained','black_centered_scaling','Scale about black-image encoding',BLUE),
            ('random','affine_group','Same rule, random encoder','#9e7965'),
            ('trained','shared_shift','Shared additive shift',RUST)]
    result={}
    for encoder,method,label,color in groups:
        data=[[float(r['latent_relative_squared_error']) for r in rows if r['encoder']==encoder and r['method']==method and float(r['ratio'])==ratio] for ratio in ratios]
        assert all(len(c)==6 for c in data)
        values=np.array(data)
        ax.plot(ratios,values.mean(axis=1),'-o',color=color,label=label,lw=2,ms=4)
        ax.fill_between(ratios,values.min(axis=1),values.max(axis=1),color=color,alpha=.1)
        result[f'{encoder}_{method}']={'mean':float(values.mean()),'min':float(values.min()),'max':float(values.max())}
    ax.set(yscale='log',xlabel='Brightness multiplier',ylabel='Relative squared latent error',xticks=ratios)
    ax.grid(axis='y',alpha=.16);ax.legend(loc='upper center',bbox_to_anchor=(.5,-.19),ncol=2,frameon=False,fontsize=9)
    fig.tight_layout();save(fig,'brightness-transfer')
    return result

def geometry_figures():
    rows=read_csv('color-discovery.csv')
    values=[float(next(r for r in rows if r['method']==method)['color_cosine'])
            for method in ['within-class diffs (class labels)','raw ICA (no labels)']]
    assert values==[.826,.716]
    fig,ax=plt.subplots(figsize=(8.5,2.6))
    ax.barh([0,1],values,height=.45,color=[GREEN,BLUE])
    for row,value in enumerate(values):ax.text(value+.022,row,f'{value:.3f}',va='center',fontsize=13)
    ax.set(yticks=[0,1],yticklabels=['Uses shape labels','ICA without labels'],xlim=(0,1.05),
           xticks=[0,.25,.5,.75,1],xlabel='Alignment with the color reference · higher is closer')
    ax.invert_yaxis();ax.grid(axis='x',alpha=.15);ax.set_axisbelow(True)
    fig.tight_layout();save(fig,'color-discovery')
    d=np.load(DATA/'geometry-examples.npz')
    # One common learned direction; all digit classes were present during fitting.
    assert np.allclose(d['traversals'][:,:,1],d['images'][:,None])
    fig,axes=plt.subplots(3,3,figsize=(7.0,6.4))
    for row,label in enumerate(d['labels']):
        for col in range(3):
            ax=axes[row,col]
            ax.imshow(np.clip(d['traversals'][row,0,col],0,1),cmap='gray',vmin=0,vmax=1,interpolation='nearest')
            ax.set(xticks=[],yticks=[])
            for spine in ax.spines.values():spine.set_visible(False)
            if row==0: ax.set_title(['−1.5 SD','Original','+1.5 SD'][col],fontsize=13,pad=13)
            if col==0: ax.set_ylabel(f'Digit {label}',fontsize=13,labelpad=18)
    fig.subplots_adjust(left=.14,right=.99,top=.92,bottom=.02,wspace=.10,hspace=.12)
    save(fig,'within-class-geometry')
    a=np.load(DATA/'shape-action-examples.npz')
    assert np.max(np.abs(a['color_prediction3']-a['color_target3']))<1e-12
    fig,axes=plt.subplots(2,4,figsize=(10.5,5.7))
    for row,shape in enumerate(['Triangle','Cross']):
        for col,(key,title) in enumerate([('input','Original color'),('target3','Requested color'),('shift3','Add a fixed pixel pattern'),('prediction3','Apply a color rule')]):
            ax=axes[row,col];ax.imshow(np.clip(a['color_'+key][row],0,1),interpolation='nearest')
            ax.set(xticks=[],yticks=[])
            for spine in ax.spines.values():spine.set_visible(False)
            if row==0:ax.set_title(title,fontsize=12,pad=14)
            if col==0:ax.set_ylabel(shape,fontsize=12,labelpad=12)
    fig.subplots_adjust(left=.08,right=.995,top=.91,bottom=.02,wspace=.06,hspace=.10)
    save(fig,'shape-transfer')
    # DOM labels keep this comparison readable when the page becomes narrow.
    errors={method:np.max(np.abs(a['color_'+method]-a['color_target3']),axis=-1)
            for method in ['shift3','prediction3']}
    error_max=max(float(e.max()) for e in errors.values())
    for row,shape in enumerate(['triangle','cross']):
        for key in ['input','target3','shift3','prediction3']:
            Image.fromarray(np.round(np.clip(a['color_'+key][row],0,1)*255).astype(np.uint8)).save(ASSETS/f'color-{shape}-{key}.png')
        for method,values in errors.items():
            # Same absolute scale for both methods and both shapes; no per-image enhancement.
            rgba=plt.get_cmap('magma')(np.clip(values[row]/error_max,0,1))
            Image.fromarray(np.round(rgba[:,:,:3]*255).astype(np.uint8)).save(ASSETS/f'color-{shape}-{method}-error.png')
    ramp=plt.get_cmap('magma')(np.linspace(0,1,256)[None,:])
    Image.fromarray(np.round(ramp[:,:,:3]*255).astype(np.uint8)).save(ASSETS/'color-error-scale.png')
    print(json.dumps({'color_error_scale_max':error_max,'learned_rule_max_error':float(errors['prediction3'].max())}))

if __name__=='__main__':
    geometry_figures()
    output={'model':model_data(),'network':network_data(),'benchmarks':benchmark_data(),
            'brightness':brightness_data(),'classification':classification_data(),
            'inputDesign':input_design_data(),'transfer':transfer_data()}
    output['improvementRange']=[min(x['improvement'] for x in output['brightness']),max(x['improvement'] for x in output['brightness'])]
    (ASSETS/'study-data.json').write_text(json.dumps(output, separators=(',',':'),allow_nan=False),encoding='utf-8')
    print(json.dumps({'modelCheck':output['model']['closedFormOdeError'], 'gridCells':len(output['network']['rows']),
                      'brightnessImprovement':output['improvementRange'], 'benchmarks':{k:v['count'] for k,v in output['benchmarks'].items()}}))
