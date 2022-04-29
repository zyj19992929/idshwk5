
event http_reply(c: connection, version: string, code: count, reason: string) 
{
    SumStats::observe("count of response",  SumStats::Key($host=c$id$orig_h), SumStats::Observation($num=1));
    if (code == 404) #识别不到??
    {
        SumStats::observe("404 response", SumStats::Key($host=c$id$orig_h), SumStats::Observation($num=1));
        SumStats::observe("unique 404 response", SumStats::Key($host=c$id$orig_h), SumStats::Observation($str=c$http$uri));
    }
}


event zeek_init()
{
    local reducer1 = SumStats::Reducer($stream="count of response", $apply=set(SumStats::SUM));
    local reducer2 = SumStats::Reducer($stream="404 response", $apply=set(SumStats::SUM));
    local reducer3 = SumStats::Reducer($stream="unique 404 response",  $apply=set(SumStats::UNIQUE));
    SumStats::create([$name = "idshwk4",
                      $epoch = 10min,
                      $reducers = set(reducer1,reducer2,reducer3),
                      $epoch_result(ts: time, key: SumStats::Key, result: SumStats::Result) =
                        {
                            local ratio1 : double = result["404 response"]$sum / result["count of response"]$sum;
                            local ratio2 : double = result["unique 404 response"]$unique / result["404 response"]$sum;
                            if (result["404 response"]$sum > 2 && ratio1 > 0.2 && ratio2 > 0.5) 
                            {
                                print fmt("%s is orig_h, %.0f is the count of 404 response , %.0f is the unique count of url response 404", key$host, result["404 response"]$sum, result["unique 404 response"]$sum);
                        }}]);
}

