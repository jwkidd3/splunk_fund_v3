| eventcount summarize=false index=* index=_*
| dedup index
| table index
