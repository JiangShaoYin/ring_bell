src_bjse=shaoyin@sz21:/disk1/DATA/cn/live/taq_1min/bjse_huatech_sz21
src_xshe=shaoyin@sz21:/disk1/DATA/cn/live/taq_1min/szse_mddp_sz21
src_xshg=shaoyin@sh31:/disk1/DATA/cn/live/taq_1min/sse_ldds_sh31

target_bjse=dytech/feed/equities/cn/live/bjse/taq/1min_taq
target_xshg=dytech/feed/equities/cn/live/xshg/taq/1min_taq
target_xshe=dytech/feed/equities/cn/live/xshe/taq/1min_taq

# 5min
ultimate_target_5min=dytech/feed/equities/cn/live/taq
ultimate_target_1min=dytech/feed/equities/cn/live/1min_taq

SYNC_END_HOUR=17

function sync_merge() {
  base_dir1=$1
  base_dir2=$2
  base_dir3=$3

  target_dir1=$4
  target_dir2=$5
  target_dir3=$6

  ymdhm=$7
  ultimate_target=$8

  sync_taq "${base_dir1}/${ymdhm}" "${target_dir1}/${ymdhm}"  cn_taq_new.log &
  sync_taq "${base_dir2}/${ymdhm}" "${target_dir2}/${ymdhm}"  cn_taq_new.log &
  sync_taq "${base_dir3}/${ymdhm}" "${target_dir3}/${ymdhm}"  cn_taq_new.log &

  wait

  merge_taq "${target_dir1}/${ymdhm}" "${target_dir2}/${ymdhm}" "${target_dir3}/${ymdhm}" "${ultimate_target}/${ymdhm}"
}

function sync_taq() {
  echo "$(date +"%Y-%m-%d %H:%M:%S"): sync_taq $1 $2 $3"
  src=$1
  target=$2
  log_file=$3

  mkdir -p $(dirname $target)

  local cnt=0
  while [ ${cnt} -le ${SYNC_MAX_RETRY} ]; do
    rsync -aqz --log-file=${log_file} "${src}" "${target}"
    if [ $? -eq 0 ]; then
      return
    fi

    echo "$(date +"%Y-%m-%d %H:%M:%S"): rsync -aqz --log-file=${log_file} ${src} ${target}, cnt=${cnt} failed, retrying..."

    hour=$(TZ='Asia/Shanghai' date +"%H")
    if [[ ${hour} -gt ${SYNC_END_HOUR} ]]; then
      return
    if
    
    cnt=$((cnt+1))
    sleep 1
  done
}

function merge_taq() {
    echo "$(date +"%Y-%m-%d %H:%M:%S"): merge_taq"

    target_filename=$4
    mkdir -p $(dirname $target_filename)

    cat $1 > target_filename
    cat $2 >>  target_filename
    cat $3 >> target_filename
}


function process() {
  year=$1
  month=$2
  day=$3
  hour=$4
  minute=$5

  filename_ymdhm="${year}/${month}/${day}/${hour}${minute}"

  sync_merge "${src_bjse}" "${src_xshg}" "${src_xshe}" "${target_bjse}" "${target_xshg}" "${target_xshe}" "${filename_ymdhm}" "${ultimate_target_1min}"

  if [ $((10#${minute} % 5)) -eq 0 ]; then
    sync_merge "${src_bjse/1min/5min}" "${src_xshg/1min/5min}" "${src_xshe/1min/5min}" "${target_bjse/1min/5min}" "${target_xshg/1min/5min}" "${target_xshe/1min/5min}" "${filename_ymdhm}" "${ultimate_target_5min}"
  fi
}

process "$@"

# bash zzz.sh   $(TZ='Asia/Shanghai' date +"%Y %m %d %H %M %S")