package us.kbase.sampleservice;

import com.fasterxml.jackson.core.type.TypeReference;
import java.io.File;
import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import us.kbase.auth.AuthToken;
import us.kbase.common.service.JsonClientCaller;
import us.kbase.common.service.JsonClientException;
import us.kbase.common.service.RpcContext;
import us.kbase.common.service.UnauthorizedException;

/**
 * <p>Original spec-file module name: SampleService</p>
 * <pre>
 * A KBase module: SampleService
 * Handles creating, updating, retriving samples and linking data to samples.
 * Note that usage of the administration flags will be logged by the service.
 * </pre>
 */
public class SampleServiceClient {
    private JsonClientCaller caller;
    private String serviceVersion = null;
    private static URL DEFAULT_URL = null;
    static {
        try {
            DEFAULT_URL = new URL("https://ci.kbase.us/services/sampleservice");
        } catch (MalformedURLException mue) {
            throw new RuntimeException("Compile error in client - bad url compiled");
        }
    }

    /** Constructs a client with the default url and no user credentials.*/
    public SampleServiceClient() {
       caller = new JsonClientCaller(DEFAULT_URL);
    }


    /** Constructs a client with a custom URL and no user credentials.
     * @param url the URL of the service.
     */
    public SampleServiceClient(URL url) {
        caller = new JsonClientCaller(url);
    }
    /** Constructs a client with a custom URL.
     * @param url the URL of the service.
     * @param token the user's authorization token.
     * @throws UnauthorizedException if the token is not valid.
     * @throws IOException if an IOException occurs when checking the token's
     * validity.
     */
    public SampleServiceClient(URL url, AuthToken token) throws UnauthorizedException, IOException {
        caller = new JsonClientCaller(url, token);
    }

    /** Constructs a client with a custom URL.
     * @param url the URL of the service.
     * @param user the user name.
     * @param password the password for the user name.
     * @throws UnauthorizedException if the credentials are not valid.
     * @throws IOException if an IOException occurs when checking the user's
     * credentials.
     */
    public SampleServiceClient(URL url, String user, String password) throws UnauthorizedException, IOException {
        caller = new JsonClientCaller(url, user, password);
    }

    /** Constructs a client with a custom URL
     * and a custom authorization service URL.
     * @param url the URL of the service.
     * @param user the user name.
     * @param password the password for the user name.
     * @param auth the URL of the authorization server.
     * @throws UnauthorizedException if the credentials are not valid.
     * @throws IOException if an IOException occurs when checking the user's
     * credentials.
     */
    public SampleServiceClient(URL url, String user, String password, URL auth) throws UnauthorizedException, IOException {
        caller = new JsonClientCaller(url, user, password, auth);
    }

    /** Constructs a client with the default URL.
     * @param token the user's authorization token.
     * @throws UnauthorizedException if the token is not valid.
     * @throws IOException if an IOException occurs when checking the token's
     * validity.
     */
    public SampleServiceClient(AuthToken token) throws UnauthorizedException, IOException {
        caller = new JsonClientCaller(DEFAULT_URL, token);
    }

    /** Constructs a client with the default URL.
     * @param user the user name.
     * @param password the password for the user name.
     * @throws UnauthorizedException if the credentials are not valid.
     * @throws IOException if an IOException occurs when checking the user's
     * credentials.
     */
    public SampleServiceClient(String user, String password) throws UnauthorizedException, IOException {
        caller = new JsonClientCaller(DEFAULT_URL, user, password);
    }

    /** Get the token this client uses to communicate with the server.
     * @return the authorization token.
     */
    public AuthToken getToken() {
        return caller.getToken();
    }

    /** Get the URL of the service with which this client communicates.
     * @return the service URL.
     */
    public URL getURL() {
        return caller.getURL();
    }

    /** Set the timeout between establishing a connection to a server and
     * receiving a response. A value of zero or null implies no timeout.
     * @param milliseconds the milliseconds to wait before timing out when
     * attempting to read from a server.
     */
    public void setConnectionReadTimeOut(Integer milliseconds) {
        this.caller.setConnectionReadTimeOut(milliseconds);
    }

    /** Check if this client allows insecure http (vs https) connections.
     * @return true if insecure connections are allowed.
     */
    public boolean isInsecureHttpConnectionAllowed() {
        return caller.isInsecureHttpConnectionAllowed();
    }

    /** Deprecated. Use isInsecureHttpConnectionAllowed().
     * @deprecated
     */
    public boolean isAuthAllowedForHttp() {
        return caller.isAuthAllowedForHttp();
    }

    /** Set whether insecure http (vs https) connections should be allowed by
     * this client.
     * @param allowed true to allow insecure connections. Default false
     */
    public void setIsInsecureHttpConnectionAllowed(boolean allowed) {
        caller.setInsecureHttpConnectionAllowed(allowed);
    }

    /** Deprecated. Use setIsInsecureHttpConnectionAllowed().
     * @deprecated
     */
    public void setAuthAllowedForHttp(boolean isAuthAllowedForHttp) {
        caller.setAuthAllowedForHttp(isAuthAllowedForHttp);
    }

    /** Set whether all SSL certificates, including self-signed certificates,
     * should be trusted.
     * @param trustAll true to trust all certificates. Default false.
     */
    public void setAllSSLCertificatesTrusted(final boolean trustAll) {
        caller.setAllSSLCertificatesTrusted(trustAll);
    }
    
    /** Check if this client trusts all SSL certificates, including
     * self-signed certificates.
     * @return true if all certificates are trusted.
     */
    public boolean isAllSSLCertificatesTrusted() {
        return caller.isAllSSLCertificatesTrusted();
    }
    /** Sets streaming mode on. In this case, the data will be streamed to
     * the server in chunks as it is read from disk rather than buffered in
     * memory. Many servers are not compatible with this feature.
     * @param streamRequest true to set streaming mode on, false otherwise.
     */
    public void setStreamingModeOn(boolean streamRequest) {
        caller.setStreamingModeOn(streamRequest);
    }

    /** Returns true if streaming mode is on.
     * @return true if streaming mode is on.
     */
    public boolean isStreamingModeOn() {
        return caller.isStreamingModeOn();
    }

    public void _setFileForNextRpcResponse(File f) {
        caller.setFileForNextRpcResponse(f);
    }

    public String getServiceVersion() {
        return this.serviceVersion;
    }

    public void setServiceVersion(String newValue) {
        this.serviceVersion = newValue;
    }

    /**
     * <p>Original spec-file function name: create_sample</p>
     * <pre>
     * Create a new sample or a sample version.
     * </pre>
     * @param   params   instance of type {@link us.kbase.sampleservice.CreateSampleParams CreateSampleParams}
     * @return   parameter "address" of type {@link us.kbase.sampleservice.SampleAddress SampleAddress}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public SampleAddress createSample(CreateSampleParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<SampleAddress>> retType = new TypeReference<List<SampleAddress>>() {};
        List<SampleAddress> res = caller.jsonrpcCall("SampleService.create_sample", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_sample</p>
     * <pre>
     * Get a sample. If the version is omitted the most recent sample is returned.
     * </pre>
     * @param   params   instance of type {@link us.kbase.sampleservice.GetSampleParams GetSampleParams}
     * @return   parameter "sample" of type {@link us.kbase.sampleservice.Sample Sample}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Sample getSample(GetSampleParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<Sample>> retType = new TypeReference<List<Sample>>() {};
        List<Sample> res = caller.jsonrpcCall("SampleService.get_sample", args, retType, true, false, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_samples</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.sampleservice.GetSamplesParams GetSamplesParams}
     * @return   parameter "samples" of list of type {@link us.kbase.sampleservice.Sample Sample}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public List<Sample> getSamples(GetSamplesParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<List<Sample>>> retType = new TypeReference<List<List<Sample>>>() {};
        List<List<Sample>> res = caller.jsonrpcCall("SampleService.get_samples", args, retType, true, false, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_sample_acls</p>
     * <pre>
     * Get a sample's ACLs.
     * </pre>
     * @param   params   instance of type {@link us.kbase.sampleservice.GetSampleACLsParams GetSampleACLsParams}
     * @return   parameter "acls" of type {@link us.kbase.sampleservice.SampleACLs SampleACLs}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public SampleACLs getSampleAcls(GetSampleACLsParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<SampleACLs>> retType = new TypeReference<List<SampleACLs>>() {};
        List<SampleACLs> res = caller.jsonrpcCall("SampleService.get_sample_acls", args, retType, true, false, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: update_sample_acls</p>
     * <pre>
     * Update a sample's ACLs.
     * </pre>
     * @param   params   instance of type {@link us.kbase.sampleservice.UpdateSampleACLsParams UpdateSampleACLsParams}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public void updateSampleAcls(UpdateSampleACLsParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<Object> retType = new TypeReference<Object>() {};
        caller.jsonrpcCall("SampleService.update_sample_acls", args, retType, false, true, jsonRpcContext, this.serviceVersion);
    }

    /**
     * <p>Original spec-file function name: update_samples_acls</p>
     * <pre>
     * Update the ACLs of many samples.
     * </pre>
     * @param   params   instance of type {@link us.kbase.sampleservice.UpdateSamplesACLsParams UpdateSamplesACLsParams}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public void updateSamplesAcls(UpdateSamplesACLsParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<Object> retType = new TypeReference<Object>() {};
        caller.jsonrpcCall("SampleService.update_samples_acls", args, retType, false, true, jsonRpcContext, this.serviceVersion);
    }

    /**
     * <p>Original spec-file function name: replace_sample_acls</p>
     * <pre>
     * Completely overwrite a sample's ACLs. Any current ACLs are replaced by the provided
     * ACLs, even if empty, and gone forever.
     * The sample owner cannot be changed via this method.
     * </pre>
     * @param   params   instance of type {@link us.kbase.sampleservice.ReplaceSampleACLsParams ReplaceSampleACLsParams}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public void replaceSampleAcls(ReplaceSampleACLsParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<Object> retType = new TypeReference<Object>() {};
        caller.jsonrpcCall("SampleService.replace_sample_acls", args, retType, false, true, jsonRpcContext, this.serviceVersion);
    }

    /**
     * <p>Original spec-file function name: get_metadata_key_static_metadata</p>
     * <pre>
     * Get static metadata for one or more metadata keys.
     *         The static metadata for a metadata key is metadata *about* the key - e.g. it may
     *         define the key's semantics or denote that the key is linked to an ontological ID.
     *         The static metadata does not change without the service being restarted. Client caching is
     *         recommended to improve performance.
     * </pre>
     * @param   params   instance of type {@link us.kbase.sampleservice.GetMetadataKeyStaticMetadataParams GetMetadataKeyStaticMetadataParams}
     * @return   parameter "results" of type {@link us.kbase.sampleservice.GetMetadataKeyStaticMetadataResults GetMetadataKeyStaticMetadataResults}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public GetMetadataKeyStaticMetadataResults getMetadataKeyStaticMetadata(GetMetadataKeyStaticMetadataParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<GetMetadataKeyStaticMetadataResults>> retType = new TypeReference<List<GetMetadataKeyStaticMetadataResults>>() {};
        List<GetMetadataKeyStaticMetadataResults> res = caller.jsonrpcCall("SampleService.get_metadata_key_static_metadata", args, retType, true, false, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: create_data_link</p>
     * <pre>
     * Create a link from a KBase Workspace object to a sample.
     *         The user must have admin permissions for the sample and write permissions for the
     *         Workspace object.
     * </pre>
     * @param   params   instance of type {@link us.kbase.sampleservice.CreateDataLinkParams CreateDataLinkParams}
     * @return   parameter "results" of type {@link us.kbase.sampleservice.CreateDataLinkResults CreateDataLinkResults}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public CreateDataLinkResults createDataLink(CreateDataLinkParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<CreateDataLinkResults>> retType = new TypeReference<List<CreateDataLinkResults>>() {};
        List<CreateDataLinkResults> res = caller.jsonrpcCall("SampleService.create_data_link", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: propagate_data_links</p>
     * <pre>
     * Propagates data links from a previous sample to the current (latest) version
     *         The user must have admin permissions for the sample and write permissions for the
     *         Workspace object.
     * </pre>
     * @param   params   instance of type {@link us.kbase.sampleservice.PropagateDataLinkParams PropagateDataLinkParams}
     * @return   parameter "results" of type {@link us.kbase.sampleservice.PropagateDataLinkResults PropagateDataLinkResults}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public PropagateDataLinkResults propagateDataLinks(PropagateDataLinkParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<PropagateDataLinkResults>> retType = new TypeReference<List<PropagateDataLinkResults>>() {};
        List<PropagateDataLinkResults> res = caller.jsonrpcCall("SampleService.propagate_data_links", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: expire_data_link</p>
     * <pre>
     * Expire a link from a KBase Workspace object.
     *         The user must have admin permissions for the sample and write permissions for the
     *         Workspace object.
     * </pre>
     * @param   params   instance of type {@link us.kbase.sampleservice.ExpireDataLinkParams ExpireDataLinkParams}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public void expireDataLink(ExpireDataLinkParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<Object> retType = new TypeReference<Object>() {};
        caller.jsonrpcCall("SampleService.expire_data_link", args, retType, false, true, jsonRpcContext, this.serviceVersion);
    }

    /**
     * <p>Original spec-file function name: get_data_links_from_sample</p>
     * <pre>
     * Get data links to Workspace objects originating from a sample.
     *         The user must have read permissions to the sample. Only Workspace objects the user
     *         can read are returned.
     * </pre>
     * @param   params   instance of type {@link us.kbase.sampleservice.GetDataLinksFromSampleParams GetDataLinksFromSampleParams}
     * @return   parameter "results" of type {@link us.kbase.sampleservice.GetDataLinksFromSampleResults GetDataLinksFromSampleResults}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public GetDataLinksFromSampleResults getDataLinksFromSample(GetDataLinksFromSampleParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<GetDataLinksFromSampleResults>> retType = new TypeReference<List<GetDataLinksFromSampleResults>>() {};
        List<GetDataLinksFromSampleResults> res = caller.jsonrpcCall("SampleService.get_data_links_from_sample", args, retType, true, false, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_data_links_from_sample_set</p>
     * <pre>
     * Get all workspace object metadata linked to samples in a list of samples or sample set
     * refs. Returns metadata about links to data objects. A batch version of
     * get_data_links_from_sample.
     * The user must have read permissions to the sample. A permissions error is thrown when a
     * sample is found that the user has no access to.
     * </pre>
     * @param   params   instance of type {@link us.kbase.sampleservice.GetDataLinksFromSampleSetParams GetDataLinksFromSampleSetParams}
     * @return   parameter "results" of type {@link us.kbase.sampleservice.GetDataLinksFromSampleResults GetDataLinksFromSampleResults}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public GetDataLinksFromSampleResults getDataLinksFromSampleSet(GetDataLinksFromSampleSetParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<GetDataLinksFromSampleResults>> retType = new TypeReference<List<GetDataLinksFromSampleResults>>() {};
        List<GetDataLinksFromSampleResults> res = caller.jsonrpcCall("SampleService.get_data_links_from_sample_set", args, retType, true, false, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_data_links_from_data</p>
     * <pre>
     * Get data links to samples originating from Workspace data.
     *         The user must have read permissions to the workspace data.
     * </pre>
     * @param   params   instance of type {@link us.kbase.sampleservice.GetDataLinksFromDataParams GetDataLinksFromDataParams}
     * @return   parameter "results" of type {@link us.kbase.sampleservice.GetDataLinksFromDataResults GetDataLinksFromDataResults}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public GetDataLinksFromDataResults getDataLinksFromData(GetDataLinksFromDataParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<GetDataLinksFromDataResults>> retType = new TypeReference<List<GetDataLinksFromDataResults>>() {};
        List<GetDataLinksFromDataResults> res = caller.jsonrpcCall("SampleService.get_data_links_from_data", args, retType, true, false, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_sample_via_data</p>
     * <pre>
     * Get a sample via a workspace object. Read permissions to a workspace object grants
     * read permissions to all versions of any linked samples, whether the links are expired or
     * not. This method allows for fetching samples when the user does not have explicit
     * read access to the sample.
     * </pre>
     * @param   params   instance of type {@link us.kbase.sampleservice.GetSampleViaDataParams GetSampleViaDataParams}
     * @return   parameter "sample" of type {@link us.kbase.sampleservice.Sample Sample}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Sample getSampleViaData(GetSampleViaDataParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<Sample>> retType = new TypeReference<List<Sample>>() {};
        List<Sample> res = caller.jsonrpcCall("SampleService.get_sample_via_data", args, retType, true, false, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_data_link</p>
     * <pre>
     * Get a link, expired or not, by its ID. This method requires read administration privileges
     * for the service.
     * </pre>
     * @param   params   instance of type {@link us.kbase.sampleservice.GetDataLinkParams GetDataLinkParams}
     * @return   parameter "link" of type {@link us.kbase.sampleservice.DataLink DataLink}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public DataLink getDataLink(GetDataLinkParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<DataLink>> retType = new TypeReference<List<DataLink>>() {};
        List<DataLink> res = caller.jsonrpcCall("SampleService.get_data_link", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: validate_samples</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.sampleservice.ValidateSamplesParams ValidateSamplesParams}
     * @return   parameter "results" of type {@link us.kbase.sampleservice.ValidateSamplesResults ValidateSamplesResults}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public ValidateSamplesResults validateSamples(ValidateSamplesParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<ValidateSamplesResults>> retType = new TypeReference<List<ValidateSamplesResults>>() {};
        List<ValidateSamplesResults> res = caller.jsonrpcCall("SampleService.validate_samples", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    public Map<String, Object> status(RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        TypeReference<List<Map<String, Object>>> retType = new TypeReference<List<Map<String, Object>>>() {};
        List<Map<String, Object>> res = caller.jsonrpcCall("SampleService.status", args, retType, true, false, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }
}
